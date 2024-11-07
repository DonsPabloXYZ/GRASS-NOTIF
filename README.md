# 🌿 Grass Notifier Telegram Bot 🌿

Automate notifications from the Grass API right to your Telegram! This bot retrieves essential account details and sends scheduled notifications, so users stay updated with minimal effort.

---

## 🚀 Features

- **Automatic Notifications**: Receive updates every hour on key account info.
- **Token Management**: Easily set and store unique authentication tokens for each user.
- **Real-Time Updates**: Get notified of your total points, uptime, stage, and more.
- **User-Friendly**: Intuitive commands for quick setup and interaction.

---

## 📦 Requirements

Ensure the following are installed and configured before running the bot:

1. **Python Packages**:
   - `requests` - For API interactions.
   - `python-telegram-bot==13.7` - For Telegram bot functions (note: using version 13.7 as requested).
   
   Install packages by running:
   ```bash
   pip install requests python-telegram-bot==13.7
2. **Telegram Bot Token**:
   - Replace the placeholder in the code with your bot token from BotFather.
3. **API Access**:
The bot uses the following endpoints:
   - https://api.getgrass.io/epochEarnings?input=%7B%22isLatestOnly%22:false%7D
   - https://api.getgrass.io/retrieveUser
   - Channel Permissions:
   - Make sure your bot has permission to message users in your channel.

## 📜 Commands

| Command       | Description                                                               |
|---------------|---------------------------------------------------------------------------|
| `/start`      | Welcomes the user and provides a tutorial link for token setup.           |
| `/set "token"` | Saves the user’s authentication token and activates notifications.       |

## 🔧 Setup Instructions
   - git clone https://github.com/DonsPabloXYZ/GRASS-NOTIF
   - cd GRASS-NOTIF
   - python main.py

## 📞 Support
For any questions or issues, please contact us on our Telegram channel: @airdroptodayreal

