from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
import os
from bancoDB import DBHelper
from telegram import ReplyKeyboardMarkup

DO = 0

def start(bot, update):
    update.message.reply_text('Hi! Luckily, this bot works. Now, let\'s do stuff!')
    helper = DBHelper()
    if helper.account_exists(update.message.chat_id):
        return DO
    else:
        helper.create_account(update.message.chat_id, "{} {}".format(update.message.from_user.first_name, update.message.from_user.second_name), 0)
        date_account = helper.show_account(update.message.chat_id)
        update.message.reply_text(date_account)


def delete_account(bot, update):

    reply_keyboard = [['Si', 'No']]
    update.message.reply_text("¿Seguro que deseas eliminar tu cuenta?",
                              reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    # if reply_markup == 'Si':
    #     helper = DBHelper()
    #     helper.delete_account(update.message.chat_id)
    #     if helper.account_exists(update.message.chat_id):
    #         update.message.reply_text("Upss Parece que tenemos un problema. Intenta de nuevo mas tarde.")
    #     else:
    #         update.message.reply_text("Cuenta eliminada!")



def what_to_do(bot, update):
    pass

def main():
    TOKEN = "382499494:AAEJrdhHmXy46VV-RrBv0xmkIJps09eJyD4"
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    delete_handler  = CommandHandler('delete', delete_account)
    dispatcher.add_handler(delete_handler)

    PORT = int(os.environ.get('PORT', '5000'))
    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN)
    updater.bot.set_webhook("https://kodefest6.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()