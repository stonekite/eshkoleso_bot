from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler
from utils.updater import updater
from handlers.scheduler import schedule_actions
from handlers.start import start_handler
from handlers.callback_handler import callback_handler, message_handler
import logging


def main():
    logging.basicConfig(format='%(asctime)s [%(levelname)s]: %(message)s', level=logging.INFO)
    schedule_actions()
    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
    updater.dispatcher.add_handler(MessageHandler(filters=None, callback=message_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
