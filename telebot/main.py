import telebot
from extensions import APIException, Convertor
from config import TOKEN, exchanges
import traceback

exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}
TOKEN = "5689961767:AAFiCYf1Rbx4k3T-BkeSOJ6Wdk_dz-GQMXk"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Здравствуйте! Чтобы начать работу введите комманду боту в следующем формате: \n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Слишком много параметров!')
        
        answer = Convertor.get_price(*values)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользоваеля. \n{e}" )
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Не удалось обработать команду\n{e}" )
    else:
        bot.reply_to(message,answer)

bot.polling()
