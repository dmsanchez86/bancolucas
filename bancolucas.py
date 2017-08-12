# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler, MessageHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup
import bancoFilter

DELETE = 0
OPTIONS = 0


def create_account(bot, update):
    helper = DBHelper()
    if helper.account_exists(update.message.chat_id):
        bot.send_message(chat_id=update.message.chat_id, text='Ya tiene cuenta')
        return ConversationHandler.END
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Bienvenido. En este momento nuestro equipo crea su cuenta.')
        helper.create_account(update.message.chat_id, "{}".format(update.message.from_user.first_name), 0, True)
        date_account = helper.show_account(update.message.chat_id)
        dates = "Su cuenta se creo con éxito, " \
            "los datos son:" \
            "\nNumero de Cuenta: {} \nNombre del Cliente: {} " \
            "\nSaldo en Cuenta: {}".format(date_account[0], date_account[1], date_account[2])
        update.message.reply_text(dates)
        return ConversationHandler.END


def show_account(bot, update):
    helper = DBHelper()
    exists_acc = helper.account_exists(update.message.chat_id)
    if exists_acc:
        date_account = helper.show_account(update.message.chat_id)
        dates = "Numero de Cuenta: {} \nNombre del Cliente: {} \nSaldo en Cuenta: {}".format(date_account[0], date_account[1], date_account[2])
        if date_account[3] == False:
            update.message.reply_text("Cuenta desavtivada '/activar' para activar.")
        else:
            update.message.reply_text(dates)
    else:
        update.message.reply_text("No existe la cuenta. '/start' para crear una nueva cuenta.")


def sure_desactivate_account(bot, update):
    reply_keyboard = [["Si"], ["No"]]
    update.message.reply_text("¿Seguro de que desea desactivar su cuenta?",
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return DELETE


def desactivate_account(bot, update):
    helper = DBHelper()
    helper.desactivate_account(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text="Cuenta desactivada. '/activar' para volver a usar su cuenta.")
    return ConversationHandler.END

def active_account(bot, update):
    helper = DBHelper()
    helper.activate_account(update.message.chat_id)
    bot.send_message(chat_id=update.message.chat_id, text="Cuenta activada.")


def options(bot, update):
    helper = DBHelper()
    if helper.account_exists(update.message.chat_id) and helper.show_account(update.message.chat_id)[3]:
        reply_keyboard = [["Ver nuestros servicios"], ["Desactivar cuenta"]]
        update.message.reply_text("¿Que deseas hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return OPTIONS
    elif helper.account_exists(update.message.chat_id):
        reply_keyboard = [["Ver nuestros servicios"], ["Activar cuenta"]]
        update.message.reply_text("¿Que deseas hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return OPTIONS
    elif not helper.account_exists(update.message.chat_id):
        reply_keyboard = [["Crear cuenta"], ["Ver nuestros servicios"]]
        update.message.reply_text("¿Que deseas hacer?", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        return OPTIONS

def services(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Nuestros servicios:")
    return ConversationHandler.END


def cancel(bot, update):
    pass

def main():
    TOKEN = "382499494:AAEJrdhHmXy46VV-RrBv0xmkIJps09eJyD4"
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    options_handler = ConversationHandler(
        entry_points=[CommandHandler('opciones', options), CommandHandler('start', options)],
        states={
            OPTIONS: [MessageHandler(bancoFilter.filter_service, services),
                      MessageHandler(bancoFilter.filter_new_account, create_account),
                      MessageHandler(bancoFilter.filter_desactivate_account, desactivate_account)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(options_handler)

    delete_handler = ConversationHandler(
        entry_points=[CommandHandler('desactivar', sure_desactivate_account)],

        states={
            DELETE: [RegexHandler('^(Si|No)$', desactivate_account)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(delete_handler)

    active_handler = CommandHandler('activar', active_account)
    dispatcher.add_handler(active_handler)

    show_handler = CommandHandler('vercuenta', show_account)
    dispatcher.add_handler(show_handler)

    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    updater.bot.set_webhook("https://kodefest6.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()