import requests
import logging
import time

from pymongo import MongoClient
from datetime import datetime, timezone, timedelta

from config import (
    LEETCODE_USERNAME,
    BOT_TOKEN,
    CHAT_ID,
    MONGO_URI
)

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# TIMEZONES
# --------------------------------------------------

IST = timezone(timedelta(hours=5, minutes=30))
UTC = timezone.utc

# --------------------------------------------------
# MONGODB
# --------------------------------------------------

client = MongoClient(MONGO_URI)

db = client["leetcode_bot"]

state_collection = db["bot_state"]

# --------------------------------------------------
# DEFAULT STATE
# --------------------------------------------------

DEFAULT_STATE = {
    "_id": "main_state",
    "streak": 0,
    "last_success_day_utc": "",
    "last_success_notified": "",
    "last_reminder_sent": ""
}

# --------------------------------------------------
# LOAD STATE
# --------------------------------------------------

def load_state():

    state = state_collection.find_one({
        "_id": "main_state"
    })

    if not state:

        state_collection.insert_one(DEFAULT_STATE)

        return DEFAULT_STATE

    return state

# --------------------------------------------------
# SAVE STATE
# --------------------------------------------------

def save_state(state):

    state_collection.replace_one(
        {"_id": "main_state"},
        state,
        upsert=True
    )

# --------------------------------------------------
# RETRY REQUESTS
# --------------------------------------------------

def retry_request(method, url, **kwargs):

    last_exception = None

    for attempt in range(3):

        try:

            response = requests.request(
                method,
                url,
                timeout=20,
                **kwargs
            )

            response.raise_for_status()

            return response

        except Exception as e:

            logger.warning(
                f"Request failed ({attempt+1}/3): {e}"
            )

            last_exception = e

            time.sleep(2)

    raise last_exception

# --------------------------------------------------
# TELEGRAM
# --------------------------------------------------

def send_telegram_message(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }

    retry_request(
        "POST",
        url,
        data=payload
    )

    logger.info("Telegram message sent")

# --------------------------------------------------
# LEETCODE GRAPHQL
# --------------------------------------------------

GRAPHQL_URL = "https://leetcode.com/graphql"

# --------------------------------------------------
# FETCH SUBMISSIONS
# --------------------------------------------------

def get_recent_submissions():

    query = """
    query recentSubmissionList($username: String!) {
        recentSubmissionList(username: $username) {
            title
            titleSlug
            timestamp
            statusDisplay
        }
    }
    """

    variables = {
        "username": LEETCODE_USERNAME
    }

    response = retry_request(
        "POST",
        GRAPHQL_URL,
        json={
            "query": query,
            "variables": variables
        }
    )

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])

    return data["data"]["recentSubmissionList"]

# --------------------------------------------------
# UTC DAY
# --------------------------------------------------

def get_current_utc_day():

    return str(datetime.now(UTC).date())

# --------------------------------------------------
# VALID ACCEPTED SUBMISSION
# --------------------------------------------------

def has_valid_submission_today(submissions):

    current_day = get_current_utc_day()

    for sub in submissions:

        # ONLY ACCEPTED

        if sub["statusDisplay"] != "Accepted":
            continue

        ts = int(sub["timestamp"])

        submission_day = str(
            datetime.fromtimestamp(ts, UTC).date()
        )

        if submission_day == current_day:
            return sub

    return None

# --------------------------------------------------
# STREAK UPDATE
# --------------------------------------------------

def update_streak():

    state = load_state()

    current_day = get_current_utc_day()

    # increment ONLY ONCE per UTC day

    if state["last_success_day_utc"] != current_day:

        state["streak"] += 1

        state["last_success_day_utc"] = current_day

        save_state(state)

        logger.info(
            f"Streak incremented to {state['streak']}"
        )

    return state["streak"]

# --------------------------------------------------
# SUCCESS DUPLICATE PROTECTION
# --------------------------------------------------

def should_send_success_notification():

    state = load_state()

    current_day = get_current_utc_day()

    return (
        state["last_success_notified"]
        != current_day
    )

# --------------------------------------------------
# MARK SUCCESS NOTIFIED
# --------------------------------------------------

def mark_success_notified():

    state = load_state()

    state["last_success_notified"] = (
        get_current_utc_day()
    )

    save_state(state)

# --------------------------------------------------
# REMINDER LEVELS
# --------------------------------------------------

def get_reminder_level():

    now = datetime.now(IST)

    h = now.hour
    m = now.minute

    if h == 22:
        return "soft"

    if h == 23 and m < 30:
        return "medium"

    if h == 23 and m >= 50:
        return "final"

    if h == 0:
        return "utc-check"

    if h == 1:
        return "extra"

    if h == 2:
        return "aggressive"

    if h == 3:
        return "last-chance"

    if h == 4:
        return "streak-lost"

    return "unknown"

# --------------------------------------------------
# REMINDER DUPLICATE PROTECTION
# --------------------------------------------------

def reminder_key(level):

    return (
        f"{get_current_utc_day()}-{level}"
    )

def should_send_reminder(level):

    state = load_state()

    return (
        state["last_reminder_sent"]
        != reminder_key(level)
    )

def mark_reminder_sent(level):

    state = load_state()

    state["last_reminder_sent"] = (
        reminder_key(level)
    )

    save_state(state)

# --------------------------------------------------
# BUILD REMINDER MESSAGE
# --------------------------------------------------

def build_message(level, streak):

    messages = {

        "soft":
            f"🚨*LeetCode Reminder*\n\nNo accepted submission detected today.\n🔥 Current streak: *{streak}*",

        "medium":
            f"🚨🚨*11 PM Alert*\n\nStill no accepted submission.\n🔥 Protect your *{streak}-day* streak!",

        "final":
            f"🚨🚨🚨 *FINAL WARNING*\n\nVery little time remains before UTC reset.\n🔥 Current streak: *{streak}*",

        "utc-check":
            f"🚨🚨🚨🚨*UTC Validation Check*\n\nNo accepted submission found yet.",

        "extra":
            f"🚨🚨🚨🚨🚨*1 AM Reminder*\n\nRecovery window still available.",

        "aggressive":
            f"🚨🚨🚨🚨🚨🚨*2 AM Alert*\n\nSolve one accepted problem NOW.",

        "last-chance":
            f"🚨🚨🚨🚨🚨🚨🚨*LAST CHANCE*\n\nFinal opportunity to save your streak.",

        "streak-lost":
            f"🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨*STREAK LOST*\n\nNo accepted UTC-day submission found.\nYour streak has been reset to 0."
    }

    return messages[level]

# --------------------------------------------------
# SUCCESS MESSAGE
# --------------------------------------------------

def send_success_message(submission, streak):

    message = (
        f"✅ *LeetCode Completed*\n\n"
        f"• {submission['title']}\n\n"
        f"🔥 Current streak: *{streak}*"
    )

    send_telegram_message(message)

# --------------------------------------------------
# RESET STREAK
# --------------------------------------------------

def reset_streak():

    state = load_state()

    state["streak"] = 0

    save_state(state)

    logger.info("Streak reset")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    logger.info("Bot started")

    try:

        submissions = get_recent_submissions()

        valid_submission = (
            has_valid_submission_today(
                submissions
            )
        )

        # ------------------------------------------
        # SUCCESS CASE
        # ------------------------------------------

        if valid_submission:

            streak = update_streak()

            if should_send_success_notification():

                send_success_message(
                    valid_submission,
                    streak
                )

                mark_success_notified()

            logger.info(
                "Success flow completed"
            )

            return

        # ------------------------------------------
        # FAILURE CASE
        # ------------------------------------------

        level = get_reminder_level()

        state = load_state()

        streak = state["streak"]

        if level == "streak-lost":

            reset_streak()

        message = build_message(
            level,
            streak
        )

        if should_send_reminder(level):

            send_telegram_message(message)

            mark_reminder_sent(level)

        logger.info(
            f"Reminder flow completed: {level}"
        )

    except Exception as e:

        logger.exception("Bot crashed")

        try:

            send_telegram_message(
                f"❌ Bot Error:\n{str(e)}"
            )

        except:
            pass

if __name__ == "__main__":
    main()