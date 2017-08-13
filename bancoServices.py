# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

ADD_BALANCE = 0
ADD_BALANCE_NUMBER = 1
GET_BALANCE = 0

def services(bot, update):
    reply_keyboard = [["Add fondos"], ["Ver Saldo"]]

    response = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text("¿Que quieres hacer?", reply_markup=response)

    if response == "Ver Saldo":
        return GET_BALANCE

    return ADD_BALANCE

def transfer(bot, update):
    pass

def cancel(bot, update):
    pass

def add_balance(bot, update):
    update.message.reply_text("Digita el total a añadir")
    return ADD_BALANCE_NUMBER

def get_balance(bot, update):
    update.message.reply_text("Su saldo es")
    return ConversationHandler.END


def add_balance_logic(bot, update):
    helper = DBHelper()
    sum = helper.show_account(update.message.chat_id)[2] + int(update.message.text)
    helper.add_balance(sum, update.message.chat_id)
    update.message.reply_text("Su saldo es {}".format(helper.show_account(update.message.chat_id)[2]))


add_balance_handler = ConversationHandler(entry_points=[MessageHandler(bancoFilter.filter_add_balance, add_balance)],
                                          states={ADD_BALANCE: [MessageHandler(bancoFilter.filter_number, add_balance)],
                                                  ADD_BALANCE_NUMBER: [MessageHandler(bancoFilter.filter_number, add_balance_logic)],
                                                  GET_BALANCE: [MessageHandler(bancoFilter.filter_get_balance, get_balance)]},
                                          fallbacks=[CommandHandler('cancel', cancel)])

