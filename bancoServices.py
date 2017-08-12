# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

TRANSFER = 0
def services(bot, update):
    reply_keyboard = [["Tansferencias"]]
    update.message.reply_text("¿Que deseas hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TRANSFER

def transfer(bot, update):
    pass

def cancel(bot, update):
    pass


services_handler = ConversationHandler(
    entry_points=[MessageHandler(bancoFilter.filter_service, services)],
    states={
        TRANSFER:[MessageHandler(bancoFilter.filter_transfer, transfer)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)
