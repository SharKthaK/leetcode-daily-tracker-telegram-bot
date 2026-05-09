# 🤖 LeetCode Daily Tracker Bot using GitHub Actions

[![Python](https://img.shields.io/badge/python-3.11-blue?style=for-the-badge)](https://www.python.org/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Free%20CI-orange?style=for-the-badge)](https://github.com/actions)
[![MongoDB Atlas](https://img.shields.io/badge/MongoDB%20Atlas-Free%20Tier-green?style=for-the-badge)](https://www.mongodb.com/cloud/atlas)
[![Telegram Bot API](https://img.shields.io/badge/Telegram-Bot%20API-blueviolet?style=for-the-badge)](https://core.telegram.org/bots)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

> 🎯 **A fully automated, production-ready LeetCode streak tracker and reminder bot** designed to help you maintain a daily LeetCode streak by automatically checking for accepted submissions and sending escalating Telegram reminders—entirely on the cloud with **zero infrastructure costs**.

---

## 💰 Completely Free to Deploy & Run

This project runs on **100% free services**:

| Service | Cost | Why It Works |
|---------|------|-------------|
| **MongoDB Atlas** | 🆓 Free | Free tier cluster is sufficient for all streak data |
| **GitHub Actions** | 🆓 Free | Public repositories get unlimited free minutes |
| **GitHub Actions** (Private) | 💵 Minimal | Private repos: ~300-500 minutes/month (still under GitHub's free plan) |
| **Telegram Bot API** | 🆓 Free | No cost for bot operations |
| **LeetCode API** | 🆓 Free | Public GraphQL API available |

**No credit card required. No hidden fees. No maintenance costs.** Deploy once and let it run forever! 🚀

---

## 📖 Quick Navigation

- [💰 Completely Free](#-completely-free-to-deploy--run)
- [🎯 Purpose](#-purpose)
- [✨ Features](#-features)
- [🌍 Timezone & Scheduling](#-timezone--scheduling-ist--utc)
- [⚙️ Tech Stack](#-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Setup Guide](#-setup-guide)
- [🔄 GitHub Actions Deployment](#-github-actions-deployment)
- [📊 Edge Cases Handled](#-edge-cases-handled)
- [🔒 Security & Production](#-security-notes)
- [🤝 Contributing](#-support--contributing)

---

### 🤖 What This Bot Does

The bot **automatically checks your LeetCode submissions** multiple times throughout the night and sends **escalating reminders** to help you maintain your daily streak. It validates using LeetCode's UTC dates and is fully idempotent-safe for GitHub's automatic retries and manual reruns.

---

## 🎯 Purpose

**Maintain your LeetCode streak automatically.** This bot helps you solve at least one LeetCode problem every day by:

- 🔍 **Automatically checking** for accepted submissions
- 📱 **Sending escalating Telegram reminders** if you haven't solved anything yet
- 🔐 **Tracking streaks in MongoDB** (persistent across restarts)
- ⏰ **Running on a precise schedule** using GitHub Actions
- 🌍 **Handling timezone edge cases** correctly (UTC-based streak logic)

**No manual intervention needed.** Set it up once, deploy it, and let it run forever.

---

## ✨ Features

### 🔄 Automated Daily LeetCode Tracking

Checks your LeetCode profile automatically using the **LeetCode GraphQL API**. Zero manual updates needed.

---

### 🚨 Multi-Stage Reminder System

If no accepted submission is found, escalating reminders throughout the night:

| ⏰ Time (IST) | 📬 Reminder Type | 📝 Purpose |
|:-----:|:------|:------|
| 10:00 PM | 🟢 Soft reminder | Gentle nudge to start solving |
| 11:00 PM | 🟡 Medium reminder | Time is running out |
| 11:50 PM | 🔴 Final warning | Last chance before midnight UTC |
| 12:30 AM | 🔵 UTC validation | Check if solved after midnight IST |
| 1:00 AM | 🟠 Extra reminder | Still time (if in your timezone) |
| 2:00 AM | 🔴 Aggressive reminder | Urgency increases |
| 3:00 AM | ⚫ Last chance reminder | Final opportunity |
| 4:00 AM | 🟣 Very last chance reminder | Only 1.5 hours remaining |
| 5:29 AM | 💀 Streak lost | Streak reset notification |

---

### 🔒 UTC-Safe Streak Logic

LeetCode internally uses UTC dates. This bot correctly handles all edge cases:

✅ Late-night submissions (after midnight IST, before UTC rollover)  
✅ After-midnight solves (problem solved after 12:00 AM IST)  
✅ UTC date boundaries (correct streak increments at UTC midnight)  
✅ Timezone edge cases (no false streak breaks)

---

### ✔️ Accepted-Only Validation

Only submissions marked **`Accepted`** count toward your streak.

- ❌ Wrong Answer submissions → ignored
- ❌ Time Limit Exceeded (TLE) → ignored
- ❌ Runtime Error → ignored
- ✅ Accepted → counts toward streak

---

### 🗄️ MongoDB Persistent Storage

Permanently stores in **MongoDB Atlas**:

- 🔥 Streak count
- 📅 Last successful UTC day
- 🔔 Duplicate reminder state
- ✅ Duplicate success notification state

Full cloud persistence makes the bot **safe across restarts, GitHub runner failures, and manual reruns**.

---

### 🛡️ Duplicate Protection

Prevents:

- 📬 Duplicate reminders
- ✅ Duplicate success notifications
- 🔥 Duplicate streak increments
- 🔄 GitHub Actions retry spam
- ⏯️ Manual rerun spam

---

### ☁️ Fully Cloud Automated

Uses **GitHub Actions** for scheduling:

- 🤖 Runs automatically every day (no setup required after deployment)
- 💾 No VPS or local machine needed
- 🌐 Zero infrastructure management
- 🔒 Secure secrets handled by GitHub

---

## ⚙️ Tech Stack

| 🛠️ Technology | 📌 Purpose |
|:---|:---|
| **Python 3.11** | Core bot logic & API interactions |
| **GitHub Actions** | Cloud-based scheduling & automation |
| **MongoDB Atlas** | Persistent streak data storage |
| **Telegram Bot API** | User notifications & alerts |
| **LeetCode GraphQL API** | Fetch submission data |

---

## 📁 Project Structure

```
leetcode-reminder-bot/
├── .github/
│   └── workflows/
│       └── reminder.yaml              # GitHub Actions schedule
├── .gitignore                        # Exclude secrets
├── config.py                         # Configuration constants
├── main.py                           # Core bot logic
├── requirements.txt                  # Python dependencies
├── CHANGELOG.md                      # Release history
├── .env.example                      # Template for secrets
├── .env                             # Local secrets (git-ignored)
└── README.md                        # This file


```

---

## 🌍 Timezone & Scheduling (IST / UTC)

### 📌 Key Points

- 🕐 All human-readable times in this README are in **India Standard Time (IST, UTC+5:30)**
- 🌐 Bot's streak validation uses **UTC** (LeetCode's internal standard)
- 💻 Code uses `IST = timezone(timedelta(hours=5, minutes=30))` for reminder timing
- 🔄 Submission checks use UTC for consistency

### 🔧 Convert to Your Timezone

Pick one of these options:

**Option 1: Update workflow cron entries**
- Copy `.github/workflows/reminder.yaml`
- Calculate UTC cron times for your timezone
- Replace cron values and deploy

**Option 2: Change bot timezone**
- Open `main.py` and modify: `IST = timezone(timedelta(hours=..., minutes=...))`
- Update this README accordingly

**Option 3: Use an LLM** (Easiest! 🤖)
- Copy `.github/workflows/reminder.yaml`
- Ask an LLM to convert cron times to your timezone
- Paste the converted cron entries back

All options preserve UTC-based streak logic while matching your local schedule.

### 📋 Copy-Paste Prompt for LLM Timezone Conversion

```
I have a GitHub Actions workflow for a LeetCode reminder bot. The schedule is written in IST UTC+5:30 in `.github/workflows/reminder.yaml`, but I want the reminder times converted to my local timezone.

Please do the following:
1. Read the full workflow file.
2. Convert each cron schedule from UTC to my local timezone.
3. Keep the reminder order, comments, and behavior the same.
4. Return the updated YAML only, ready to paste back into the workflow file.

Important:
- Do not remove any jobs, steps, or environment variables.
- Keep the bot's UTC-based streak logic unchanged.
- Make sure the converted cron values match the same reminder times in my timezone.

My timezone is: [PASTE YOUR TIMEZONE HERE]
```

---

## 🚀 Setup Guide

### Step 1️⃣: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/leetcode-daily-tracker-bot.git

cd leetcode-daily-tracker-bot
```

---

### Step 2️⃣: Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 3️⃣: Create Telegram Bot

Open: [https://t.me/BotFather](https://t.me/BotFather)

Create a bot and obtain:

- 🔑 **BOT_TOKEN**

---

### Step 4️⃣: Get Telegram Chat ID

1. Send a message to your bot
2. Open: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
3. Find the chat ID:

```json
"chat": {
  "id": 123456789
}
```

That number is your **CHAT_ID**.

---

### Step 5️⃣: Create MongoDB Atlas Cluster

1. Create free cluster: [https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
2. Create database user
3. Allow network access
4. Copy MongoDB URI

#### 🔐 MongoDB Network Access Setup

Since GitHub Actions uses dynamic cloud IPs, MongoDB Atlas must allow access from all IPs.

**Steps:**
1. Go to: `MongoDB Atlas → Security → Network Access → Add IP Address`
2. Add: `0.0.0.0/0`

This allows GitHub Actions runners to connect successfully.

---

### Step 6️⃣: Configure Environment Variables

Create a `.env` file by copying `.env.example`:

**Windows CMD:**
```cmd
copy .env.example .env
```

**Linux / macOS:**
```bash
cp .env.example .env
```

Then replace the placeholder values inside `.env` with your actual credentials:

```env
LEETCODE_USERNAME=your_leetcode_username
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id
MONGO_URI=your_mongodb_connection_string
```

> ⚠️ `.env` is excluded using `.gitignore` to keep your secrets private and secure.

---

### Step 7️⃣: Run Locally

```bash
python main.py
```

---

## 🔄 GitHub Actions Deployment

### Deploy Step 1️⃣: Push Repository

```bash
git init

git add .

git commit -m "Production ready LeetCode reminder bot"
```

Connect repository:

```bash
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

Push:

```bash
git branch -M main

git push -u origin main
```

---

### Deploy Step 2️⃣: Add GitHub Secrets

Open: **Repository → Settings → Secrets and variables → Actions**

Add these secrets:

| 🔐 Secret Name | 📋 Value |
|---|---|
| `LEETCODE_USERNAME` | Your LeetCode username |
| `BOT_TOKEN` | Telegram bot token |
| `CHAT_ID` | Telegram chat ID |
| `MONGO_URI` | MongoDB connection string |

---

### Deploy Step 3️⃣: Run Workflow Manually

Open: **Actions → LeetCode Reminder Bot → Run workflow**

---

## 📊 MongoDB State Example

```json
{
  "_id": "main_state",
  "streak": 2,
  "last_success_day_utc": "2026-05-09",
  "last_success_notified": "2026-05-09",
  "last_reminder_sent": ""
}
```

---

## ⏱️ Workflow Schedule

GitHub Actions automatically runs at these IST times:

| ⏰ IST Time | 🎯 Purpose |
|:---|:---|
| 10 PM | Soft reminder |
| 11 PM | Medium reminder |
| 11:50 PM | Final warning |
| 12:30 AM | UTC validation |
| 1 AM | Extra reminder |
| 2 AM | Aggressive reminder |
| 3 AM | Last chance |
| 4 AM | Very last chance reminder |
| 5:29 AM | Streak lost |

---

## 💬 Example Telegram Messages

### ✅ Success Message

```
✅ LeetCode Completed

• Two Sum

🔥 Current streak: 8
```

---

### ⚠️ Reminder Message

```
⚠️ LeetCode Reminder

No accepted submission detected today.
🔥 Current streak: 8
```

---

## 📊 Edge Cases Handled

The bot safely handles multiple real-world edge cases:

| 📋 Scenario | ✅ Behavior |
|---|---|
| Multiple accepted submissions in one day | Streak increments only once |
| Same problem solved repeatedly | No duplicate streak increments |
| Wrong Answer / TLE submissions | Ignored |
| GitHub Actions retry | No duplicate notifications |
| Manual reruns | Safe and idempotent |
| Solve after midnight IST | Correctly handled using UTC |
| Duplicate success messages | Prevented |
| Duplicate reminders | Prevented |
| MongoDB persistence across restarts | Supported |
| GitHub runner restarts | Safe |
| Empty submission list | Reminder flow activates |
| Multiple reminders at same level | Prevented |
| Temporary API/network failure | Retry logic included |
| Re-submission of same accepted problem | Ignored for streak counting |

---

## 🏆 Production Features

### ✨ Implemented

- ✅ UTC-safe streak tracking
- ✅ Accepted-only validation
- ✅ MongoDB persistence
- ✅ Duplicate reminder prevention
- ✅ Duplicate success prevention
- ✅ Retry-safe API requests
- ✅ GitHub retry safety
- ✅ Manual rerun safety
- ✅ Cloud automation
- ✅ Comprehensive logging
- ✅ Idempotent architecture

---

## 🔒 Security Notes

### Never Upload Secrets

Never push:
```
.env
```

Your `.gitignore` already prevents this.

### Store Secrets Safely

Secrets should only be stored in:
```
GitHub Secrets
```

---

## 📚 API References

- 🤖 **Telegram Bot API**: [https://core.telegram.org/bots/api](https://core.telegram.org/bots/api)
- 📊 **LeetCode GraphQL API**: [https://leetcode.com/graphql](https://leetcode.com/graphql)
- 🗄️ **MongoDB Atlas**: [https://www.mongodb.com/atlas/database](https://www.mongodb.com/atlas/database)

---

## 📄 License

MIT License

---

## 🤝 Support & Contributing

Thank you for checking out this project - **contributions and stars are much appreciated!** ⭐

### How to Contribute

- ⭐ **Star this repo** to show support and help others discover it
- 🐛 **Report issues** for bugs or feature requests using the GitHub Issues tab
- 💡 **Open a Pull Request** to contribute code or docs

### Suggested Workflow

1. Fork the repository
2. Create a branch: `git checkout -b feat/your-feature`
3. Make small, focused commits and ensure the bot still runs locally
4. Push your branch and open a PR with a clear title and description

### First Contributions Welcome!

Small doc improvements, badges, typo fixes, and readability changes are great first contributions - don't hesitate to open a small PR.

### Need Help with Timezone Conversion?

If you're unsure how to convert workflow cron times to your timezone:
- Copy `.github/workflows/reminder.yaml` and paste it into an LLM prompt asking for conversion
- Or open an issue and tell us your timezone - we'll prepare a converted workflow for you!

---

## 👨‍💻 Author & Creator

<div align="center">

### **Sarthak Chakraborty**

🚀 **Full-Stack Developer** | 🤖 **AI/ML Enthusiast** | 🎯 **Open Source Contributor**

---

**📧 Email:** [sarthak@vacantvectors.com](mailto:sarthak@vacantvectors.com)

**🌐 Portfolio:** [Sarthak Chakraborty](https://sarthakchakraborty.in)

---

> _"Building tools to help developers maintain their coding streaks and build consistent habits."_ 💪

</div>

---

<div align="center">

## 🎉 Happy Streak Tracking! 🎉

**Made with ❤️ by Sarthak Chakraborty**

### ⭐ If this project helped you, please consider giving it a star!

**[⭐ Star on GitHub](https://github.com/SharKthaK/leetcode-daily-tracker-bot)** • **[📧 Contact](mailto:sarthak@vacantvectors.com)** • **[🌐 Portfolio](https://sarthakchakraborty.in)**

</div>
