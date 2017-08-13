# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

ADD_BALANCE = 0
ADD_BALANCE_NUMBER = 1
GET_BALANCE = 2
WITHDRAW = 3
WITHDRAW_NUMBER = 4
ACCOUNT_INFO = 5

def services(bot, update):
    reply_keyboard = [["Agregar Saldo"], ["Ver Saldo"], ["Retirar"], ["Cuenta"]]

    response = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    update.message.reply_text("¿Que quieres hacer?", reply_markup=response)

    if response == "Ver Saldo":
        return GET_BALANCE
    elif response == "Retirar":
        return WITHDRAW
    elif response == "Cuenta"
        return ACCOUNT_INFO

    return ADD_BALANCE

def transfer(bot, update):
    pass

def cancel(bot, update):
    pass

def add_balance(bot, update):
    update.message.reply_text("Digita el total a añadir")
    return ADD_BALANCE_NUMBER

def get_balance(bot, update):
    helper = DBHelper()
    balance = helper.get_balance(update.message.chat_id)
    update.message.reply_text("Su saldo es {}".format(balance[0]))
    return ConversationHandler.END


def add_balance_logic(bot, update):
    helper = DBHelper()
    sum = helper.show_account(update.message.chat_id)[2] + int(update.message.text)
    helper.add_balance(sum, update.message.chat_id)
    update.message.reply_text("Su saldo es ${}".format(helper.show_account(update.message.chat_id)[2]))
    return ConversationHandler.END

def get_info(bot, update)
    helper = DBHelper()
    account_info = helper.show_account(update.message.chat_id)
    update.message.reply_text("El número de cuenta es {}".format(account_info[0]))
    return ConversationHandler.END


def withdraw(bot, update):
    update.message.reply_text("Digita el total a retirar")
    return WITHDRAW_NUMBER

def withdraw_logic(bot, update):
    helper = DBHelper()
    withdrawal = helper.show_account(update.message.chat_id)[2] - int(update.message.text)
    if withdrawal < 0:
        update.message.reply_text("Fondos insuficientes")
    else:
        helper.withdraw(withdrawal, update.message.chat_id)
    update.message.reply_text("Su nuevo saldo es ${}".format(helper.show_account(update.message.chat_id)[2]))
    return ConversationHandler.END


add_balance_handler = ConversationHandler(entry_points=[MessageHandler(bancoFilter.filter_add_balance, add_balance), MessageHandler(bancoFilter.filter_get_balance, get_balance)
    , MessageHandler(bancoFilter.filter_withdraw, withdraw), MessageHandler(bancoFilter.filter_account, get_info)],
                                          states={ADD_BALANCE: [MessageHandler(bancoFilter.filter_number, add_balance)],
                                                  ADD_BALANCE_NUMBER: [MessageHandler(bancoFilter.filter_number, add_balance_logic)],
                                                  GET_BALANCE: [MessageHandler(bancoFilter.filter_get_balance, get_balance)],
                                                  WITHDRAW: [MessageHandler(bancoFilter.filter_withdraw, withdraw)],
                                                  WITHDRAW_NUMBER: [MessageHandler(bancoFilter.filter_number, withdraw_logic)],
                                                  ACCOUNT_INFO: [MessageHandler(bancoFilter.filter_account, get_info)]},
                                          fallbacks=[CommandHandler('cancel', cancel)], allow_reentry=True)
