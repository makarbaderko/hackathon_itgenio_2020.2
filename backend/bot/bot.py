import config
import telebot

token = config.API_KEY
bot = telebot.TeleBot(token)

keyboard1 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard1.row('Клиент', 'Продавец', "Курьер")

keyboard2 = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
keyboard2.row("Сделать заказ", "Проверить статус заказа")



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
        msg = bot.reply_to(message, 'Отлично, что бы Вы хотели сделать?', reply_markup=keyboard2)
        bot.register_next_step_handler(msg, process_client_2)
    else:
        bot.send_message(message.chat.id, 'In development')

def process_client_2(message):
    l = str(message).split()
    text = l[-2]
    text = text[1:]
    if text == "Сделать":
        msg = bot.reply_to(message, 'Cкажи, пожалуйста, свое имя')
        bot.register_next_step_handler(msg, process_client_3)
def process_client_3(message):
    pass

bot.polling()