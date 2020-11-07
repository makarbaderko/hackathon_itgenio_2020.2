import config
import telebot
from db_manager import SQL


token = config.API_KEY
bot = telebot.TeleBot(token)
db = SQL('database.db')

keyboard1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard1.row('Клиент', 'Продавец', "Курьер")

keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard2.row("Сделать заказ", "Проверить статус заказа")

current_client = {"username": None, "name": None, "surname": None, "phone": None, "adress": None}

@bot.message_handler(commands=['start'])
def start_message(message):
    msg = bot.reply_to(message, 'Привет, скажи, пожалуйста, кто ты?', reply_markup=keyboard1)
    bot.register_next_step_handler(msg, process_client_1)

@bot.message_handler(content_types=['text'])
def process_client_1(message):
    l = str(message).split()
    text = l[-1]
    text = text[1:-3]
    if text == "Клиент":
        msg = bot.reply_to(message, 'Отлично, что бы ты хотел сделать?', reply_markup=keyboard2)
        bot.register_next_step_handler(msg, process_client_2)
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
            print(1)
        else:
            print(0)
        #msg = bot.reply_to(message, 'Cкажи, пожалуйста, свое имя')
        #bot.register_next_step_handler(msg, process_client_3)
def process_client_3(message):
    l = str(message).split()
    text = l[-1]
    text = text[1:-3]
    print(text)

bot.polling()