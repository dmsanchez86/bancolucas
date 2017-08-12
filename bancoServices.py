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
    bot.send_message(chat_id=update.message.chat_id, text="¿Cuanto quieres agregar?")
    return ADD_BALANCE


def add_balance_logic(bot, update):
    helper = DBHelper()
    balance = helper.show_account(update.message.chat_id)[2] + update.message.text
    helper.add_balance(balance, update.message.chat_id)
    update.message.reply_text("Tu saldo es de {}".format(helper.show_account(update.message.chat_id)[2]))
    return ConversationHandler.END


services_handler = ConversationHandler(
    entry_points=[MessageHandler(bancoFilter.filter_service, services)],
    states={
        TRANSFER:[MessageHandler(bancoFilter.filter_transfer, transfer)],
        ADD_BALANCE:[MessageHandler(bancoFilter.filter_add_balance, add_balance)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)



