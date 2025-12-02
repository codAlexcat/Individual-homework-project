# Бтблиотеки:
"""
1. pip install python-telegram-bot==20.7 pip install sqlite3-binary (Если SQLite не работает у тебя локально)
2. from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
___
BOT_TOKEN = "ТОКЕН_ОТ_BOTFATHER"
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Бот работает!")
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
Запусти и убедись, что бот отвечает
___
1. Создай: db.py - там будет храниться команда для управления пользователями

"""






