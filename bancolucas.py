# -*- coding: utf-8 -*-
from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup

DELETE = 0


def start(bot, update):

    helper = DBHelper()
    if helper.account_exists(update.message.chat_id):
        update.message.reply_text("Ya tienes cuenta")
    else:
        update.message.reply_text('Bienvenido. En este momento nuestro equipo crea su cuenta.')
        helper.create_account(update.message.chat_id, "{}".format(update.message.from_user.first_name), 0)
        date_account = helper.show_account(update.message.chat_id)
        dates = "Su cuenta se creo con éxito, " \
                "los datos son:" \
                "\nNumero de Cuenta: {} \nNombre del Cliente: {} " \
                "\nSaldo en Cuenta: {}".format(date_account[0], date_account[1], date_account[2])
        update.message.reply_text(dates)


def show_account(bot, update):
    helper = DBHelper()
    date_account = helper.show_account(update.message.chat_id)
    dates = "Numero de Cuenta: {} \nNombre del Cliente: {} \nSaldo en Cuenta: {}".format(date_account[0], date_account[1], date_account[2])
    update.message.reply_text(dates)


def sure_delete_account(bot, update):
    reply_keyboard = [["Si"], ["No"]]
    update.message.reply_text("¿Seguro de eliminar su cuenta?",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard))
    return DELETE


def delete_account(bot, update):
    helper = DBHelper()


    if update.message.text == 'Si' and helper.account_exists(update.message.chat_id):
        if not helper.account_exists(update.message.chat_id):
            update.message.chat_id("Su cuenta ha sido eliminada.")
            return ConversationHandler.END
        else:
            update.message.chat_id("Ups, ocurrio un problema '/delete' para volver a intentarlo.")
            return ConversationHandler.END
    elif not helper.account_exists(update.message.chat_id):
        update.message.reply_text("Usted no tiene aun una cuenta, nuestro equipo lo invita a unirse. Solo debe digitar '/start'")
        return ConversationHandler.END
    else:
        update.message.reply_text("Gracias por seguir con nosotros")
        return ConversationHandler.END


def cancel(bot, update):
    pass


def main():
    TOKEN = "382499494:AAEJrdhHmXy46VV-RrBv0xmkIJps09eJyD4"
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher

    delete_handler = ConversationHandler(
        entry_points=[CommandHandler('delete', sure_delete_account)],

        states={
            DELETE: [RegexHandler('^(Si|No)$', delete_account)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(delete_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

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