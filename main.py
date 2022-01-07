from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler
from handlers.start import start_handler
from handlers.callback_handler import callback_handler, message_handler
from utils.keys import bot_token
import logging

def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    updater = Updater(bot_token)
    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    updater.dispatcher.add_handler(MessageHandler(filters=None, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
