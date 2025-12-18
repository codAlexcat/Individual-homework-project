# Импортируем библиотеки и модули
import telebot
import random
from telebot import types

# Токен бота
TOKEN = "8421918578:AAFwSywLpGeSyINjYD4auP6iS3A8NBpcm2w"

# Словарь для хранения игр
user_games = {}  # формат: {user_id: {'number': X, 'attempts': Y}}

# запускаем бота
bot = telebot.TeleBot(TOKEN)

# функционал на команду start
@bot.message_handler(commands=['start'])
def start(message):
    # Получаем имя пользователя
    name = message.from_user.first_name
    # Выводим сообщение о функционале бота
    text = f"Привет, {name}!\nЯ игровой бот! \n\n🎮 Команды: \n/dice - Бросить кости \n/game - Камень-ножницы-бумага \n/number - Угадай число \n/help - Помощь"
    bot.send_message(message.chat.id, text)

# Игра в кости
@bot.message_handler(commands=['dice'])
def dice(message):
    # Генерируем два рандомных числа для костей
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    faces = {1: "⚀", 2: "⚁", 3: "⚂", 4: "⚃", 5: "⚄", 6: "⚅"}
    # Выводим сообщение о том какие кости выпали и их сумму
    text = f"{faces[dice1]} {faces[dice2]} \nВыпало: {dice1} и {dice2} \nСумма: {dice1 + dice2}"
    bot.send_message(message.chat.id, text)


# Камень-ножницы-бумага
@bot.message_handler(commands=['game'])
def game(message):
    # Создаем кнопки для игры в камень ножницы бумага
    markup = types.InlineKeyboardMarkup(row_width=3)
    btn1 = types.InlineKeyboardButton("✊", callback_data="rock")
    btn2 = types.InlineKeyboardButton("✌️", callback_data="scissors")
    btn3 = types.InlineKeyboardButton("✋", callback_data="paper")
    # Добавляем эти три кнопки в одну строку
    markup.add(btn1, btn2, btn3)
    # Выводим сообщение с кнопками под ним
    bot.send_message(message.chat.id, "Выбери:", reply_markup=markup)

# Обработка кнопок игры
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_choice = call.data
    # бот рандомно выбирает из списка что он выберет
    bot_choice = random.choice(['rock', 'scissors', 'paper'])
    # Делаем простую проверку на совпадения
    if user_choice == bot_choice:
        result = "🤝 Ничья!"
    elif (user_choice == 'rock' and bot_choice == 'scissors') or (
            user_choice == 'scissors' and bot_choice == 'paper') or (user_choice == 'paper' and bot_choice == 'rock'):
        result = "🎉 Ты победил!"
    else:
        result = "😢 Бот победил!"

    emoji = {'rock': '✊', 'scissors': '✌️', 'paper': '✋'}

    text = f"Ты: {emoji[user_choice]} \nБот: {emoji[bot_choice]}\n\n"
    text += result
    # Редактируем уже ранее отправленное сообщение на результат игры
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id)

# Угадай число
@bot.message_handler(commands=['number'])
def guess_number(message):
    user_id = message.chat.id
    secret_number = random.randint(1, 10)
    # Сохраняем игру в глобальный словарь
    user_games[user_id] = {
        'number': secret_number,
        'attempts': 0
    }
    # Выводим сообщение
    text = f"Я загадал число от 1 до 10!\nПопробуй угадать!\nОтправь мне число от 1 до 10:"
    bot.send_message(message.chat.id, text)

# Обработка чисел (для игры угадай число)
# Декоратор который обрабатывает исключительно те сообщения которые состоят только из цыфор
# func=lambda m: m.text.isdigit() - Возврощает True если все сообщения цыфры, и False если все символы не цыфры
@bot.message_handler(func=lambda m: m.text.isdigit())
def check_number(message):
    user_id = message.chat.id

    # Проверяем, активная ли игра
    if user_id not in user_games:
        bot.send_message(user_id, "Сначала начни игру командой /number!")
        return

    try:
        user_guess = int(message.text)
        game_data = user_games[user_id]  # получаем данные игры
        secret_number = game_data['number']
        game_data['attempts'] += 1  # увеличиваем счетчик попыток

        # Проверяем диапазон
        if user_guess < 1 or user_guess > 10:
            bot.send_message(user_id, "(-_-) Введи число от 1 до 10!")
            return

        # Сравниваем числа
        if user_guess == secret_number:
            attempts = game_data['attempts']
            if attempts == 1:
                reaction = "iba четко! Угадал с первой попытки!"
            elif attempts <= 3:
                reaction = "Угадал быстро!"
            else:
                reaction = "Угадал!"

            bot.send_message(user_id, f"{reaction}\nЧисло было: {secret_number}\nПопыток: {attempts}")

            # Удаляем игру после победы
            del user_games[user_id]

        elif user_guess < secret_number:
            bot.send_message(user_id, f"Мое число БОЛЬШЕ чем {user_guess}")
        else:
            bot.send_message(user_id, f"Мое число МЕНЬШЕ чем {user_guess}")

    except ValueError:
        bot.send_message(user_id, "Пожалуйста, введи нормальное число!")


# Помощь
@bot.message_handler(commands=['help'])
def help_command(message):
    text = "Помощь: \n\n/start - Начать общение \n/dice - Бросить кости \n/game - Камень-ножницы-бумага \n/number - Угадай число \n/help - Эта справка"
    bot.send_message(message.chat.id, text)


# Ответ на обычный текст
@bot.message_handler(func=lambda m: True)
def echo(message):
    name = message.from_user.first_name
    bot.send_message(message.chat.id, f"Привет, {name}! Напиши /start для начала")


# Запуск бота
print("Бот запустился иди в тг")
bot.polling(none_stop=True)

