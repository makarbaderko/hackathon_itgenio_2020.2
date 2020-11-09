import config
import telebot
from db_manager import SQL
import os

restaurants = {"12345":"abc"}
current_restaurant_id = ""
current_restaurant_key = ""

token = config.API_KEY
bot = telebot.TeleBot(token)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "database.db")
db = SQL(db_path)

keyboard1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard1.row('Клиент', 'Ресторан', "Курьер")

keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard2.row("Сделать заказ", "Проверить статус заказа")

keyboard3 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard3.row("Да, досталяйте туда же", "Нет, я сейчас введу новые")

keyboard4 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard4.row("Москва", "Санкт-Петербург")

keyboard5 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard5.row("Да, сохраняйте", "Нет, спасибо.")

keyboard6 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard6.row("KFC", "McDonalds")

keyboard7 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard7.row("Получить список заказов", "Заказ отдан курьеру", "Что в заказе?")

keyboard8 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard8.row("Уже зарегистрированы", "Хотим подключиться")

keyboard9 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard9.row("Cэндвичи", "Бургеры")

keyboard10 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard10.row("Баскеты", "Твистеры")

keyboard11 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard11.row("Сандерс Баскет", "Баскет Дуэт")
keyboard11.row("Домашний Баскет", "Баскет L")

keyboard12 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard12.row("Да", "Нет")

keyboard13 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard13.row("Закончить оформление заказа", "Прлолжить оформление заказа")

current_client = {"username": None, "name": None, "surname": None, "phone": None, "adress": None, "city": None}

foods = ""

current_client_for_restaurant = {"order_id": None}

@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, 'Здравствуйте, скажите, пожалуйста, кто Вы?', reply_markup=keyboard1)

    bot.register_next_step_handler(msg, process_client_1)

@bot.message_handler(content_types=['text'])
def process_client_1(message):
    l = str(message).split()
    text = l[-1]
    text = text[1:-3]
    if text == "Клиент":
        msg = bot.reply_to(message, 'Отлично, что бы Вы хотели сделать?', reply_markup=keyboard2)
        bot.register_next_step_handler(msg, process_client_2)
    if text == 'Ресторан':
        msg = bot.reply_to(message, 'Отлично! Вы уже зарегистрированы в нашей системе?', reply_markup=keyboard8)
        bot.register_next_step_handler(msg, process_restaurant_1)
    if text == "Курьер":
        pass
    else:
        bot.send_message(message.chat.id, 'In development')

def process_client_2(message):
    l = str(message).split()
    text = l[-2]
    text = text[1:]
    if text == "Сделать":
        username = ((str(message).split("""username': '""")[1]).split("'"))[0]
        current_client["username"] = username
        if db.user_exists(current_client["username"]) == True:
            msg = bot.reply_to(message, 'Вы уже заказывали у нас, можем ли мы использовать данные с прошлого заказа?', reply_markup=keyboard3)
            bot.register_next_step_handler(msg, process_client_3_yes)
        else:
            bot.send_message(message.chat.id, 'Сейчас мы попросим ввести Ваши данные, для нашей службы доставки.')
            process_client_4(message)
def process_client_3_yes(message):
    if message.text == "Нет, я сейчас введу новые":
        msg = bot.reply_to(message, 'Выберите, пожалуйста, Ваш город', reply_markup=keyboard4)
        bot.register_next_step_handler(msg, process_client_4)
    else:
        process_client_7_1(message)
def process_client_4(message):
    global current_client
    current_client["city"] = message.text
    msg = bot.reply_to(message, 'Введите, пожалуйста, Ваш адрес.')
    bot.register_next_step_handler(msg, process_client_5)
def process_client_5(message):
    global current_client
    current_client["adress"] = message.text
    msg = bot.reply_to(message, 'Введите, пожалуйста, Ваш номер телефона.')
    bot.register_next_step_handler(msg, process_client_6)
def process_client_6(message):
    global current_client
    current_client ["phone"] = message.text
    msg = bot.reply_to(message, 'Хотите ли Вы, чтобы мы сохранили Ваши данные у себя, для упрощения создания заказа Вами в будущем?', reply_markup=keyboard5)
    bot.register_next_step_handler(msg, process_client_7)
def process_client_7(message):
    if message.text == "Да, сохраняйте":
        #db.add_user(username=current_client["username"], name=current_client["name"], surname=current_client["surname"], city=current_client["city"], phone=current_client["city"], adress=current_client["adress"])
        msg = bot.reply_to(message, 'Где бы Вы хотели заказать еду?', reply_markup=keyboard6)
        bot.register_next_step_handler(msg, process_client_8)
    else:
        msg = bot.reply_to(message, 'Где бы Вы хотели заказать еду?', reply_markup=keyboard6)
        bot.register_next_step_handler(msg, process_client_8)
def process_client_7_1(message):
    #db.add_user(username=current_client["username"], name=current_client["name"], surname=current_client["surname"], city=current_client["city"], phone=current_client["city"], adress=current_client["adress"])
    msg = bot.reply_to(message, 'Где бы Вы хотели заказать еду?', reply_markup=keyboard6)
    bot.register_next_step_handler(msg, process_client_8)
def process_client_8(message):
    if message.text == "KFC":
        msg = bot.reply_to(message, 'Что бы Вы хотели заказать?', reply_markup=keyboard10)
        bot.register_next_step_handler(msg, process_client_8_1)
    if message.text == "McDonalds":
        msg = bot.reply_to(message, 'Что бы Вы хотели заказать?', reply_markup=keyboard9)
        bot.register_next_step_handler(msg, process_client_8_2)

def process_client_8_1(message):
    if message.text == "Баскеты":
        msg = bot.reply_to(message, 'Что бы Вы хотели заказать?', reply_markup=keyboard11)
        bot.register_next_step_handler(msg, process_client_9_1)
    if message.text == "Твистеры":
        pass
def process_client_8_2(message):
    if message.text == "Cэндвичи":
        pass
    if message.text == "Бургеры":
        pass

def process_client_9_1(message):
    global foods
    foods += str(message.text)
    foods += " "
    msg = bot.reply_to(message, 'Что-нибудь еще?', reply_markup=keyboard12)
    bot.register_next_step_handler(msg, process_client_10)

def process_client_10(message):
    if message.text == "Да":
        msg = bot.reply_to(message, 'Что бы Вы хотели заказать?', reply_markup=keyboard10)
        bot.register_next_step_handler(msg, process_client_8_1)
    else:
        msg = bot.reply_to(message, 'Закончим?', reply_markup=keyboard13)
        bot.register_next_step_handler(msg, process_client_11)
def process_client_11(message):
    bot.send_message(message.chat.id, "Заказ передан в службу доставки. Ожидайте. По всем вопросам звоните на +8 (800) 555-35-35")

def process_restaurant_1(message):
    if message.text == "Уже зарегистрированы":
        msg = bot.reply_to(message, 'Введите, пожалуйста, Ваш ID ресторана')
        bot.register_next_step_handler(msg, process_restaurant_1_1)
    if message.text == "Хотим подключиться":
        bot.send_message(message.chat.id, "Напишите нам в Telegram на t.me/makarbaderko для подключения к нашей сети доставки")
def process_restaurant_1_1(message):
    global current_restaurant_id
    current_restaurant_id = message.text
    msg = bot.reply_to(message, 'Введите, пожалуйста, Ваш key ресторана')
    bot.register_next_step_handler(msg, process_restaurant_1_2)

def process_restaurant_1_2(message):
    global current_restaurant_id, current_restaurant_key
    current_restaurant_key = message.text
    if restaurants[current_restaurant_id] == current_restaurant_key:
        msg = bot.reply_to(message, 'Что бы Вы хотели сделать?', reply_markup=keyboard7)
        bot.register_next_step_handler(msg, process_restaurant_2)
def process_restaurant_2(message):
    if message.text == "Получить список заказов":
        data = db.get_all_orders()
        new_data = ""
        for tupl in data:
            new_data += f"Номер заказа: {tupl[0]} Состав заказа: {tupl[1]} Курьер: {tupl[2]}\n"
        bot.send_message(message.chat.id, new_data)
        msg = bot.reply_to(message, 'Что бы Вы хотели сделать?', reply_markup=keyboard7)
        bot.register_next_step_handler(msg, process_restaurant_2)
    if message.text == "Заказ отдан курьеру":
        msg = bot.reply_to(message, 'Введите, пожалуйста, номер переданного заказа.')
        bot.register_next_step_handler(msg, process_restaurant_2_1)
    if message.text == "Что в заказе?":
        msg = bot.reply_to(message, 'Введите, пожалуйста, номер заказа, по которму идет поиск')
        bot.register_next_step_handler(msg, process_restaurant_2_2)

def process_restaurant_2_1(message):
    text = int(message.text)
    print(text)
    db.update_status(text, "BEEN_DELIVERED")
    bot.send_message(message.chat.id, "Статус заказа изменен на: Передан Курьеру")
    msg = bot.reply_to(message, 'Что бы Вы хотели сделать?', reply_markup=keyboard7)
    bot.register_next_step_handler(msg, process_restaurant_2)
def process_restaurant_2_2(message):
    data = db.get_food(message.text)
    new_data = data[0][1]
    bot.send_message(message.chat.id, new_data)
    msg = bot.reply_to(message, 'Что бы Вы хотели сделать?', reply_markup=keyboard7)
    bot.register_next_step_handler(msg, process_restaurant_2)
bot.polling()