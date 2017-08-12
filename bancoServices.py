# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

ADD_BALANCE = 0
ADD_BALANCE_NUMBER = 1
def services(bot, update):
    reply_keyboard = [["Add fondos"]]

    update.message.reply_text("¿Que quieres hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ADD_BALANCE

def transfer(bot, update):
    pass

def cancel(bot, update):
    pass

def add_balance(bot, update):
    update.message.reply_text("Digita el total a añadir")
    return ADD_BALANCE_NUMBER


def add_balance_logic(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="hi")


add_balance_handler = ConversationHandler(entry_points=[MessageHandler(bancoFilter.filter_add_balance, add_balance)],
                                          states={ADD_BALANCE: [MessageHandler(bancoFilter.filter_number, add_balance)],
                                                  ADD_BALANCE_NUMBER: [MessageHandler(bancoFilter.filter_number, add_balance_logic)]},
                                          fallbacks=[CommandHandler('cancel', cancel)])
