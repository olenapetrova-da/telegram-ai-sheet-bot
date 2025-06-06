### File: README.md

# Telegram Bot → AI → Google Sheet

## 🔧 What It Does
- User sends a structured report in Telegram
- AI extracts fields (name, date, location, quantity)
- App writes it to a Google Sheet

## 🧩 Setup

### 1. Clone the repo
```bash
git clone your-repo-url
cd your-repo
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create `.env` file
```env
# Copy and modify from example
cp .env.example .env
```
Fill in:
- `TELEGRAM_BOT_TOKEN`
- `OPENAI_API_KEY`
- `GOOGLE_SHEET_NAME`
- `GOOGLE_CREDENTIALS_JSON`

### 4. Add Google credentials
- Get JSON key from Google Cloud → Service Accounts
- Save as `credentials.json` in root folder
- Share your Google Sheet with the service account email

### 5. Run the bot
```bash
python bot.py
```

## ✅ Example Telegram Message
```
Report: Olena Petrova, 03.06.2025, Warsaw, 240 units sold
```

## 📄 Output in Google Sheet
| Name          | Date       | Location | Quantity      |
|---------------|------------|----------|---------------|
| Olena Petrova | 2025-06-03 | Warsaw   | 240 units sold |

---

You’re ready!
