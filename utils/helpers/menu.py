from typing import Union
from datetime import datetime
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ForceReply
from telegram.ext import CallbackContext
from utils.data.user_data import get_user_data
from utils.actions import Actions
from utils.helpers.misc import get_user_id
from utils.l10n import t


def get_menu(user_id: int, action: Actions=None) -> ReplyKeyboardMarkup:
    data = get_user_data(user_id)
    keyboard = []

    def add_row(*actions: list[Actions]):
        if actions:
            row = [KeyboardButton(text=t(action, user_id)) for action in actions]
            keyboard.append(row)

    if action == Actions.ADD_TIMEZONE:
        row = [KeyboardButton(text=t(Actions.ADD_TIMEZONE_SET_TIMEZONE, user_id), request_location=True)]
        keyboard.append(row)

    if not data.meds:
        add_row(Actions.ADD_MEDS)
        return ReplyKeyboardMarkup(keyboard=keyboard)

    if data.interval_reminders and \
        (not data.last_interval_reminders_start_date or \
            data.last_interval_reminders_start_date < datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)):
        add_row(Actions.START_INTERVAL_REMINDERS)

    add_row(Actions.SHOW_MEDS)
    add_row(Actions.SHOW_JOURNAL_QUESTIONS)
    add_row(Actions.SHOW_REMINDERS)
    add_row(Actions.SHOW_INTERVAL_REMINDERS)
    
    return ReplyKeyboardMarkup(keyboard=keyboard)


def update_menu(update: Update, context: CallbackContext, message: Union[str, Actions]):
    user_id = get_user_id(update)

    markup = {}

    if message == Actions.ADD_JOURNAL_TIME:
        markup = ForceReply()
    else:
        markup = get_menu(user_id, message)

    context.bot.send_message(text=t(message, user_id), chat_id=update.effective_chat.id, reply_markup=markup)
