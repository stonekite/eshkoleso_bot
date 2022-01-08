from typing import Union
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import CallbackContext
from datetime import date
from utils.data.user_data import get_user_data
from utils.actions import Actions, action_messages
from utils.helpers.misc import get_user_id
from utils.l10n import t


def get_menu(user_id: int) -> ReplyKeyboardMarkup:
    data = get_user_data(user_id)
    keyboard = []

    def add_row(*actions: list[Actions]):
        if actions:
            row = [KeyboardButton(text=t(action, user_id)) for action in actions]
            keyboard.append(row)

    if not data.meds:
        add_row(Actions.ADD_MEDS)
        return ReplyKeyboardMarkup(keyboard=keyboard)

    if data.interval_reminders and data.last_start_date < date.today():
        add_row(Actions.START_INTERVAL_REMINDERS)

    add_row(Actions.SHOW_MEDS)
    add_row(Actions.SHOW_REMINDERS)
    add_row(Actions.SHOW_INTERVAL_REMINDERS)
    
    return ReplyKeyboardMarkup(keyboard=keyboard)


def update_menu(update: Update, context: CallbackContext, message: Union[str, Actions]):
    user_id = get_user_id(update)

    menu = get_menu(user_id)

    context.bot.send_message(text=t(message, user_id), chat_id=update.effective_chat.id, reply_markup=menu)
