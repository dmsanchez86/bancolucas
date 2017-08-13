# -*- coding: utf-8 -*-
from telegram.ext import CommandHandler, ConversationHandler, MessageHandler
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter, bancolucas


ADD_BALANCE = 0
ADD_BALANCE_NUMBER = 1
GET_BALANCE = 2
WITHDRAW = 3
WITHDRAW_NUMBER = 4
ACCOUNT_INFO = 5
TRANSFERIR = 6
TRANSFERIR_MONTO = 7
TRANSFERIR_EXECUTE = 8
RETURN = 12
SHOW_TRANSFERS = 10
SHOW_TRANSFERS_LOGIC = 11
SHOW_WITHDRAWS = 9



def services(bot, update):
    reply_keyboard = [["Agregar Saldo"], ["Ver saldo"], ["Retirar"], ["Mis retiros"], ["Transferir"], ["Mis transferencias"],
                      ["Menu Principal"]]
    response = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("¿Que quieres hacer?", reply_markup=response)
    if response == "Ver saldo":
        return GET_BALANCE
    elif response == "Retirar":
        return WITHDRAW
    elif response == "Cuenta":
        return ACCOUNT_INFO
    elif response == "Transferir":
        return TRANSFERIR
    elif response == "Mis transferencias":
        return SHOW_TRANSFERS
    elif response == "Mis retiros":
        return SHOW_WITHDRAWS
    elif response == "Menu Principal":
        return RETURN

    return ADD_BALANCE


def transfer(bot, update):
    update.message.reply_text("Digite el numero de cuenta:")
    return TRANSFERIR_MONTO


id_and_monto = []


def transfer_monto(bot, update):
    helper = DBHelper()
    if update.message.text == "{}".format(update.message.chat_id):
        update.message.reply_text("No puede transferir dinero a su cuenta.")
        return ConversationHandler.END
    elif not helper.account_exists(update.message.text):
        update.message.reply_text("El numero de cuenta no existe")
    else:
        update.message.reply_text("Digite el monto a transferir:")
        global id_and_monto
        id_and_monto = [update.message.text]
        return TRANSFERIR_EXECUTE


def transfer_execute(bot, update):
    id_and_monto.append(update.message.text)
    helper = DBHelper()
    now_money = helper.show_account(update.message.chat_id)[2]
    name_user = helper.show_account(update.message.chat_id)[1]

    if now_money < int(id_and_monto[1]):
        update.message.reply_text("Saldos insuficientes.")
    else:
        now_money_recibe = helper.show_account(int(id_and_monto[0]))[2]
        helper.withdraw(now_money - int(id_and_monto[1]), update.message.chat_id)
        helper.withdraw(now_money_recibe + int(id_and_monto[1]), int(id_and_monto[0]))
        helper.transfer_to_account(update.message.chat_id, int(id_and_monto[0]), int(id_and_monto[1]), True)
        transfers = helper.get_transfers_sends(update.message.chat_id)
        last_transfer = transfers[len(transfers) - 1]
        update.message.reply_text("Su transferencia de ${} a la cuenta No.{} fue exitosa.".format(last_transfer[3],
                                                                                                  last_transfer[2]))
        bot.send_message(chat_id=int(id_and_monto[0]),
                         text="Usted ha recibido ${} del usuario {} con cuenta No.{}".format(int(id_and_monto[1]), name_user, update.message.chat_id))
    return ConversationHandler.END


def show_transfers(bot, update):
    reply_keyboard = [["Enviadas"], ["Recibidas"], ["Menu Principal"]]
    response = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)
    update.message.reply_text("Ver mis transferencias: ", reply_markup=response)
    return SHOW_TRANSFERS_LOGIC

def show_transfers_sends(bot, update):
    helper = DBHelper()
    mensaje = ""
    for transfer_item in helper.get_transfers_sends(update.message.chat_id):
        mensaje += "A el No.{} el dia {} por el monto de ${}. \n".format(transfer_item[2], transfer_item[4], transfer_item[3])

    update.message.reply_text(mensaje)


def show_transfers_entries(bot, update):
    helper = DBHelper()
    mensaje = ""
    for transfer_item in helper.get_transfers_receive(update.message.chat_id):
        mensaje += "De el No.{} el dia {} por el monto de ${}. \n".format(transfer_item[1], transfer_item[4], transfer_item[3])

    update.message.reply_text(mensaje)


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
        helper.withdraw_new(update.message.chat_id, helper.show_account(update.message.chat_id)[2], withdrawal,
                            int(update.message.text), True)
        helper.withdraw(withdrawal, update.message.chat_id)
    update.message.reply_text("Su nuevo saldo es ${}".format(helper.show_account(update.message.chat_id)[2]))
    return ConversationHandler.END


def show_withdraws(bot, update):
    helper = DBHelper()
    mensaje = ""
    for withdraw_item in helper.get_withdraws(update.message.chat_id):
        mensaje += "El día {} usted tenia ${}, retiro ${} y su saldo en cuenta fue ${}.\n".format(withdraw_item[5], withdraw_item[2],
                                                                                               withdraw_item[3], withdraw_item[4])

    update.message.reply_text(mensaje)


add_balance_handler = ConversationHandler(entry_points=
                                          [MessageHandler(bancoFilter.filter_add_balance, add_balance),
                                           MessageHandler(bancoFilter.filter_get_balance, get_balance),
                                           MessageHandler(bancoFilter.filter_withdraw, withdraw),
                                           MessageHandler(bancoFilter.filter_account, get_info),
                                           MessageHandler(bancoFilter.filter_transfer, transfer),
                                           MessageHandler(bancoFilter.filter_show_transfers, show_transfers),
                                           MessageHandler(bancoFilter.filter_show_withdraws, show_withdraws)],
                                          states={
                                              ADD_BALANCE: [MessageHandler(bancoFilter.filter_number, add_balance)],
                                              ADD_BALANCE_NUMBER: [MessageHandler(bancoFilter.filter_number, add_balance_logic)],
                                              GET_BALANCE: [MessageHandler(bancoFilter.filter_get_balance, get_balance)],
                                              WITHDRAW: [MessageHandler(bancoFilter.filter_withdraw, withdraw)],
                                              WITHDRAW_NUMBER: [MessageHandler(bancoFilter.filter_number, withdraw_logic)],
                                              ACCOUNT_INFO: [MessageHandler(bancoFilter.filter_account, get_info)],
                                              TRANSFERIR: [MessageHandler(bancoFilter.filter_transfer, transfer)],
                                              TRANSFERIR_MONTO: [MessageHandler(bancoFilter.filter_number, transfer_monto)],
                                              TRANSFERIR_EXECUTE: [MessageHandler(bancoFilter.filter_number, transfer_execute)],
                                              SHOW_TRANSFERS: [MessageHandler(bancoFilter.filter_show_transfers, show_transfers)],
                                              SHOW_TRANSFERS_LOGIC:[MessageHandler(bancoFilter.filter_show_transfers_sends, show_transfers_sends),
                                                                    MessageHandler(bancoFilter.filter_show_transfers_entries, show_transfers_entries)],
                                              RETURN: [MessageHandler(bancoFilter.filter_return, bancolucas.options)]
                                          },
                                          fallbacks=[CommandHandler('cancel', cancel)],
                                          allow_reentry=True)
