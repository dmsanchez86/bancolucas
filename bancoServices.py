# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter


ADD_BALANCE, ADD_BALANCE_NUMBER, GET_BALANCE, WITHDRAW, WITHDRAW_NUMBER, ACCOUNT_INFO, TRANSFERIR, TRANSFERIR_MONTO, TRANSFERIR_EXECUTE = range(9)

def services(bot, update):

    reply_keyboard = [["Agregar Saldo"], ["Ver Saldo"], ["Retirar"], ["Transferir"]]
    response = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("¿Que quieres hacer?", reply_markup=response)
    if response == "Ver Saldo":
        return GET_BALANCE
    elif response == "Retirar":
        return WITHDRAW
    elif response == "Cuenta":
        return ACCOUNT_INFO
    elif response == "Transferir":
        return TRANSFERIR

    return ADD_BALANCE



def transfer(bot, update):
    update.message.reply_text("Digite el numero de cuenta:")
    return TRANSFERIR_MONTO

id_and_monto = []
def transfer_monto(bot, update):
    update.message.reply_text("Digita el monto a transferir:")
    global id_and_monto
    id_and_monto = [update.message.text]
    return TRANSFERIR_EXECUTE


def transfer_execute(bot, update):
    id_and_monto.append(update.message.text)
    helper = DBHelper()
    now_money = helper.show_account(update.message.chat_id)[2]

    if now_money < int(id_and_monto[1]):
        update.message.reply_text("Saldos insuficientes.")
    else:
        helper.withdraw(now_money - int(id_and_monto[1]), update.message.chat_id)
        helper.transfer_to_account(update.message.chat_id, int(id_and_monto[0]), int(id_and_monto[1]), True)
        transfers = helper.get_transfers_sends(update.message.chat_id)
        last_transfer = transfers[len(transfers) - 1]
        update.message.reply_text("Su transferencia de ${} a la cuenta {} fue exitosa.".format(last_transfer[2], last_transfer[3]))
    return ConversationHandler.END


def cancel(bot, update):
    pass

def add_balance(bot, update):
    update.message.reply_text("Digita el total a añadir")
    return ADD_BALANCE_NUMBER

def get_balance(bot, update):
    helper = DBHelper()
    balance = helper.get_balance(update.message.chat_id)
    update.message.reply_text("Su saldo es ${}".format(balance[0]))
    return ConversationHandler.END


def add_balance_logic(bot, update):
    helper = DBHelper()
    sum = helper.show_account(update.message.chat_id)[2] + int(update.message.text)
    helper.add_balance(sum, update.message.chat_id)
    update.message.reply_text("Su saldo es ${}".format(helper.show_account(update.message.chat_id)[2]))
    return ConversationHandler.END

def get_info(bot, update):
    helper = DBHelper()
    account_info = helper.show_account(update.message.chat_id)
    update.message.reply_text("=> Información de la cuenta, " \
                "\n\n* Numero de Cuenta: {} \n* Nombre del Cliente: {} " \
                "\n* Saldo en Cuenta: ${}".format(account_info[0], account_info[1], account_info[2]))
    return ConversationHandler.END


def withdraw(bot, update):
    update.message.reply_text("Digita el total a retirar:")
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


add_balance_handler = ConversationHandler(entry_points=
                                          [MessageHandler(bancoFilter.filter_add_balance, add_balance),
                                           MessageHandler(bancoFilter.filter_get_balance, get_balance),
                                           MessageHandler(bancoFilter.filter_withdraw, withdraw),
                                           MessageHandler(bancoFilter.filter_account, get_info),
                                           MessageHandler(bancoFilter.filter_transfer, transfer)],
                                          states={
                                              ADD_BALANCE: [MessageHandler(bancoFilter.filter_number, add_balance)],
                                              ADD_BALANCE_NUMBER: [MessageHandler(bancoFilter.filter_number, add_balance_logic)],
                                              GET_BALANCE: [MessageHandler(bancoFilter.filter_get_balance, get_balance)],
                                              WITHDRAW: [MessageHandler(bancoFilter.filter_withdraw, withdraw)],
                                              WITHDRAW_NUMBER: [MessageHandler(bancoFilter.filter_number, withdraw_logic)],
                                              ACCOUNT_INFO: [MessageHandler(bancoFilter.filter_account, get_info)],
                                              TRANSFERIR: [MessageHandler(bancoFilter.filter_transfer, transfer)],
                                              TRANSFERIR_MONTO: [MessageHandler(bancoFilter.filter_number, transfer_monto)],
                                              TRANSFERIR_EXECUTE: [MessageHandler(bancoFilter.filter_number, transfer_execute)]
                                          },
                                          fallbacks=[CommandHandler('cancel', cancel)],
                                          allow_reentry=True)
