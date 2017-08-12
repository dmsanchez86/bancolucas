from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os
from bancoDB import DBHelper

def start(bot, update):
    update.message.reply_text('Hi! Luckily, this bot works. Now, let\'s do stuff!')
    helper = DBHelper()
    if helper.account_exists(update.message.chat_id):
        update.message.reply_text("Ya tienes cuenta")
    else:
        helper.create_account(update.message.chat_id, "{}".format(update.message.from_user.first_name), 0)
        date_account = helper.show_account(update.message.chat_id)
        update.message.reply_text(date_account)


def show_account(bot, update):
    helper = DBHelper()
    date_account = helper.show_account(update.message.chat_id)
    dates = "Numero de Cuenta: " + date_account[0] + "\n" + "Nombre Cliente: " + date_account[1] + "\n" + "Saldo en Cuenta: " + date_account[2]
    update.message.reply_text(dates)


def main():
    TOKEN = "382499494:AAEJrdhHmXy46VV-RrBv0xmkIJps09eJyD4"
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
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