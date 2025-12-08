
TOKEN = "7835456854:AAECv1R7M1kawfc1AHA0IaSbzFndjPs8EiU"

from telegram.ext import Application, CommandHandler

# Функция для команды /start
async def start_command(update, context):
    await update.message.reply_text("✅ Бот работает в PyCharm!")

# Функция для команды /test
async def test_command(update, context):
    await update.message.reply_text("Тест: Всё работает!")

# Главная функция
def main():
    # Создаем бота
    app = Application.builder().token(TOKEN).build()

    # Добавляем команды
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("test", test_command))

    # Запускаем
    print("=" * 40)
    print("БОТ ЗАПУЩЕН ИЗ PYCHARM!")
    print("Открой Telegram → найди бота → /start")
    print("=" * 40)

    app.run_polling()

if __name__ == "__main__":
    main()





