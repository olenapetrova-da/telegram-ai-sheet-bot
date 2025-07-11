### File bot.py

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from ai_agent import extract_data_from_text
from sheets_writer import write_to_sheet
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Хто ти, звідки, коли і скільки продав(-ла)?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_text = update.message.text
    structured = extract_data_from_text(raw_text)
    if structured:
        write_to_sheet(structured)
        await update.message.reply_text("✅ Твій звіт відправлено менеджеру.")
    else:
        await update.message.reply_text("❌ Couldn't extract structured data. Please try again.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
