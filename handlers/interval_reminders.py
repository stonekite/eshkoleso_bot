from bson import json_util as json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import CallbackContext
from utils.actions import Actions
from utils.data.interval_reminders import get_interval_reminders, add_interval_reminder, remove_interval_reminder
from utils.helpers.misc import answer_callback_query, get_user_id
from utils.l10n import t


def show_interval_reminders(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    reminders = get_interval_reminders(user_id)

    text = ""
    keyboard = [
        [
            InlineKeyboardButton(
                text=t(Actions.ADD_INTERVAL_REMINDER, user_id),
                callback_data=json.dumps({
                    "action": Actions.ADD_INTERVAL_REMINDER
                })
            )
        ]
    ]

    if reminders:
        reminder_list = "\n".join(\
            f"{i+1}. {reminder.meds.name} ({reminder.dosage}), \
            {reminder.repetitions} {t('times', user_id)} {t('every', user_id)} {reminder.interval} {t('hours', user_id)}" \
            for i, reminder in enumerate(reminders))

        text = \
f"""{t('Your interval reminders:', user_id)}

{reminder_list}"""

        keyboard[0] += [InlineKeyboardButton(
            text=t(Actions.REMOVE_MEDS, user_id),
            callback_data=json.dumps({
                "action": Actions.REMOVE_MEDS
            })
        )]
    else:
        text = t("You have no interval reminders right now.", user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_interval_reminder_start(update: Update, context: CallbackContext):
    pass


def remove_interval_reminder(update: Update, context: CallbackContext):
    pass


def start_interval_reminders(update: Update, context: CallbackContext):
    pass
