# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

OPERATIONS = 0
ADD_BALANCE = 1
def services(bot, update):
    reply_keyboard = [["Tansferencias"], ["Add fondos"]]
    update.message.reply_text("¿Que deseas hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return OPERATIONS

def transfer(bot, update):
    pass

def cancel(bot, update):
    pass

def add_balance(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="hi")
    return ADD_BALANCE

# def add_balance_logic(bot, update):
#     bot.send_message(chat_id=update.message.chat_id, text="hi")

service_handler = ConversationHandler(
    entry_points=[MessageHandler(bancoFilter.filter_service, services)],
    states={
        OPERATIONS:[MessageHandler(bancoFilter.filter_add_balance, add_balance)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)