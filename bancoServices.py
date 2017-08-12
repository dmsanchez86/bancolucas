# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

TRANSFER = 0
ADD_BALANCE = 1
def services(bot, update):
    reply_keyboard = [["Tansferencias"], ["Añadir fondos"]]
    update.message.reply_text("¿Que deseas hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TRANSFER

def transfer(bot, update):
    pass

def cancel(bot, update):
    pass

def add_balance(bot, update):
    helper = DBHelper()
    update.message.text("¿cuanto quieres agregar?")
    return ADD_BALANCE

services_handler = ConversationHandler(
    entry_points=[MessageHandler(bancoFilter.filter_service, services)],
    states={
        TRANSFER:[MessageHandler(bancoFilter.filter_transfer, transfer)],
        ADD_BALANCE:[MessageHandler(bancoFilter.filter_add_balance, add_balance)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)



