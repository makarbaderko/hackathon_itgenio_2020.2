import config
import telebot
from db_manager import SQL
import os


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

current_client = {"username": None, "name": None, "surname": None, "phone": None, "adress": None, "city": None}

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
def process_client_3_yes(message):
    if message.text == "Нет, я сейчас введу новые":
        msg = bot.reply_to(message, 'Выберите, пожалуйста, Ваш город', reply_markup=keyboard4)
        bot.register_next_step_handler(msg, process_client_4)
def process_client_4(message):
    msg = bot.reply_to(message, 'Введите, пожалуйста, Ваш адрес.')
    bot.register_next_step_handler(msg, process_client_5)
def process_client_5(message):
    current_client["city"] = message.text
    msg = bot.reply_to(message, 'Введите, пожалуйста, Ваш номер телефонв.')
    bot.register_next_step_handler(msg, process_client_6)
def process_client_6(message):
    current_client["phone"] = message.text
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

def process_client_8(message):
    print(message.text)

bot.polling()

