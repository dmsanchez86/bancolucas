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
SHOW_TRANSFERS = 9
SHOW_TRANSFERS_LOGIC = 10
RETURN = 11
ADD_RECARGA_MONTO = 12
ADD_RECARGA_EXECUTE = 13
SHOW_RECHARGES = 14
SHOW_WITHDRAWS = 15
RECARGAR = 16


def services(bot, update):
    reply_keyboard = [["Agregar Saldo"], ["Ver saldo"], ["Retirar"], ["Mis retiros"], ["Transferir"], ["Mis transferencias"], ["Recargar"],["Mis recargas"],
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
    elif response == "Recargar":
        return RECARGAR
    elif response == "Mis recargas":
        return SHOW_RECHARGES
    elif response == "Menu Principal":
        return RETURN

    return ADD_BALANCE


def transfer(bot, update):
    update.message.reply_text("Digite el N° de la cuenta:")
    return TRANSFERIR_MONTO


id_and_monto = []


def transfer_monto(bot, update):
    helper = DBHelper()
    if update.message.text == "{}".format(update.message.chat_id):
        update.message.reply_text("No se pudo transferir dinero a su cuenta.")
        return ConversationHandler.END
    elif not helper.account_exists(update.message.text):
        update.message.reply_text("El N° de la cuenta no existe")
    else:
        update.message.reply_text("Digite el monto a transferir $ ")
        global id_and_monto
        id_and_monto = [update.message.text]
        return TRANSFERIR_EXECUTE


def transfer_execute(bot, update):
    id_and_monto.append(update.message.text)
    helper = DBHelper()
    now_money = helper.show_account(update.message.chat_id)[2]
    name_user = helper.show_account(update.message.chat_id)[1]

    if now_money < int(id_and_monto[1]):
        update.message.reply_text("$$$ Saldos insuficientes.")
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
    mensaje = "=> Transferencias Enviadas\n\n"
    for transfer_item in helper.get_transfers_sends(update.message.chat_id):
        mensaje += "* Cuenta N° {} - fecha {} - monto ${}. \n".format(transfer_item[2], transfer_item[4], transfer_item[3])

    update.message.reply_text(mensaje)


def show_transfers_entries(bot, update):
    helper = DBHelper()
    mensaje = "=> Transferencias Recibidas\n\n"
    for transfer_item in helper.get_transfers_receive(update.message.chat_id):
        mensaje += "* Cuenta N° {} - fecha {} monto ${}. \n".format(transfer_item[1], transfer_item[4], transfer_item[3])

    update.message.reply_text(mensaje)


def cancel(bot, update):
    pass


def add_balance(bot, update):
    update.message.reply_text("Digita el total a añadir $")
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
                "\n\n* N° Cuenta: {} \n* Cliente: {} " \
                "\n* Saldo: ${}".format(account_info[0], account_info[1], account_info[2]))
    return ConversationHandler.END


def withdraw(bot, update):
    update.message.reply_text("Digita el monto a retirar $")
    return WITHDRAW_NUMBER


def withdraw_logic(bot, update):
    helper = DBHelper()
    withdrawal = helper.show_account(update.message.chat_id)[2] - int(update.message.text)
    if withdrawal < 0:
        update.message.reply_text("¡Fondos insuficientes!")
    else:
        helper.withdraw_new(update.message.chat_id, helper.show_account(update.message.chat_id)[2], withdrawal,
                            int(update.message.text), True)
        helper.withdraw(withdrawal, update.message.chat_id)
    update.message.reply_text("Su nuevo saldo es ${}".format(helper.show_account(update.message.chat_id)[2]))
    return ConversationHandler.END


def show_withdraws(bot, update):
    helper = DBHelper()
    mensaje = "Mis Retiros \n\n"
    for withdraw_item in helper.get_withdraws(update.message.chat_id):
        mensaje += "* Fecha: {} saldo ${}, retiro: ${} - nuevo saldo: ${}.\n".format(withdraw_item[5], withdraw_item[2],
                                                                                               withdraw_item[4], withdraw_item[3])

    update.message.reply_text(mensaje)


def add_recargar(bot, update):
    update.message.reply_text("Digite el N° de la cuenta que va a recargar:")
    return ADD_RECARGA_MONTO


id_and_monto_recarga = []

def add_recarga_monto(bot, update):
    global id_and_monto_recarga
    id_and_monto_recarga = [update.message.text]
    update.message.reply_text("Digite el monto que va a recargar:")
    return ADD_RECARGA_EXECUTE

def add_recarga_execute(bot, update):
    id_and_monto_recarga.append(update.message.text)
    helper = DBHelper()
    if helper.show_account(update.message.chat_id)[2] < int(id_and_monto_recarga[1]):
        update.message.chat_id("Saldos insuficientes.")
    else:
        helper.recharges(update.message.chat_id, id_and_monto_recarga[1],
                         helper.show_account(update.message.chat_id)[2],
                         helper.show_account(update.message.chat_id)[2] -  int(id_and_monto_recarga[1]),
                         id_and_monto_recarga[0],True)
        helper.withdraw(helper.show_account(update.message.chat_id)[2] -  int(id_and_monto_recarga[0]), update.message.chat_id)
        update.message.reply_text("Usted a recargado la cuenta numero {} "
                                  "por el valor de ${} y su saldo actual es ${}".format(id_and_monto_recarga[0], id_and_monto_recarga[1],
                                                                                       helper.show_account(update.message.chat_id)[2]))


def show_recharges(bot, update):
    helper = DBHelper()
    mensaje = ""
    for recharge_item in helper.get_recharges(update.message.chat_id):
        mensaje += "Usted recargo a {}, el monto de ${} el dia .\n".format(recharge_item[2], recharge_item[5],
                                                                                   recharge_item[6])

    update.message.reply_text(mensaje)


add_balance_handler = ConversationHandler(entry_points=
                                          [MessageHandler(bancoFilter.filter_add_balance, add_balance),
                                           MessageHandler(bancoFilter.filter_get_balance, get_balance),
                                           MessageHandler(bancoFilter.filter_withdraw, withdraw),
                                           MessageHandler(bancoFilter.filter_account, get_info),
                                           MessageHandler(bancoFilter.filter_transfer, transfer),
                                           MessageHandler(bancoFilter.filter_show_transfers, show_transfers),
                                           MessageHandler(bancoFilter.filter_show_withdraws, show_withdraws),
                                           MessageHandler(bancoFilter.filter_recargar, add_recargar),
                                           MessageHandler(bancoFilter.filter_show_recharges, show_recharges)],
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
                                              RETURN: [MessageHandler(bancoFilter.filter_return, bancolucas.options)],
                                              ADD_RECARGA_MONTO: [MessageHandler(bancoFilter.filter_number, add_recarga_monto)],
                                              ADD_RECARGA_EXECUTE: [MessageHandler(bancoFilter.filter_number, add_recarga_execute)]
                                          },
                                          fallbacks=[CommandHandler('cancel', cancel)],
                                          allow_reentry=True)
