from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import os
from bancoDB import DBHelper

def start(bot, update):
    helper = DBHelper()
    if helper.account_exists(update.message.chat_id):
        update.message.reply_text('hii')
    else:
        update.message.reply_text('creando cuenta...')


def cancel(bot, update):
    pass

def main():
    TOKEN = "382499494:AAEJrdhHmXy46VV-RrBv0xmkIJps09eJyD4"
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.set_webhook("https://kodefest6.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()