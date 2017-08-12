from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

def services(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Nuestros servicios:")
    return ConversationHandler.END

def exchange_cash(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Escriba el numero de la cuenta a la cual va a transferir el dinero: ")
    return 1

def transfer(bot, update):
    update.message.reply_text("Va a tansferir")