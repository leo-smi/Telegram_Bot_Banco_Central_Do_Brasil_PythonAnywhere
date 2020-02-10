# -*- coding: utf-8 -*
from flask import Flask, request
import telebot
from telebot import types
from bc.bancocentral import Cambio, Selic, Inflacao

# TELEGRAM BOT API PARAMETERS
token = "SeuTokenAqui"
bot = telebot.TeleBot(token, threaded=False)
bot.remove_webhook()
url = 'https://seu_usuario_aqui.pythonanywhere.com/'
bot.set_webhook(url = url)

# FLASK HANDLE
app = Flask(__name__)
@app.route('/', methods=["POST"])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# OPTIONS THAT REPLY MENU
@bot.message_handler(commands=['start'])
def startCommand(message):
    bot.send_message(message.chat.id, 'Olá *' + message.chat.first_name + '*!' , parse_mode='Markdown', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, text = 'Por favor acesse o /menu')

@bot.message_handler(commands=['cambio', 'selic', 'inflacao'])
def cambio(msg):

    cambio   = Cambio()
    selic    = Selic()
    inflacao = Inflacao()

    def sendMessage(msg, texto):
        return bot.send_message(msg.chat.id, texto)

    if msg.text == '/cambio':
        sendMessage(msg, 'Dólar compra: R$ {}\nDólar venda: R$ {}'.format(          cambio.get_dolar_compra(),      cambio.get_dolar_venda()))
        sendMessage(msg, 'Dólar PTAX compra: R$ {}\nDólar PTAX venda: R$ {}'.format(cambio.get_dolar_compra_ptax(), cambio.get_dolar_venda_ptax()))
        sendMessage(msg, 'Euro compra: R$ {}\nEuro venda: R$ {}'.format(            cambio.get_euro_compra(),       cambio.get_euro_venda()))
        sendMessage(msg, 'Euro compra PTAX: R$ {}\nEuro venda PTAX: R$ {}'.format(  cambio.get_euro_compra_ptax(),  cambio.get_euro_venda_ptax()))
    if msg.text == '/selic':
        sendMessage(msg, 'Taxa selic meta: {}%\nTaxa selic real: {}%'.format(       selic.get_selic_meta(),  selic.get_selic_real()))
    if msg.text == '/inflacao':
        sendMessage(msg, 'Inflacao meta: {}%\nInflação acumulada {}%'.format(       inflacao.get_meta_tax(), inflacao.get_acumulada_tax()))

# MENU WITH BUTTONS
@bot.message_handler(commands=["menu"])
def menu(message):
    keyboard        = types.ReplyKeyboardMarkup(row_width = 2, resize_keyboard=True)
    button_cambio   = types.KeyboardButton(text = '/cambio')
    button_selic    = types.KeyboardButton(text = '/selic')
    button_inflacao = types.KeyboardButton(text = '/inflacao')
    keyboard.add(button_cambio, button_selic, button_inflacao)
    bot.send_message(message.chat.id, text = "Por favor, escolha uma opção no Menu", reply_markup = keyboard)
