from datetime import datetime, timedelta
from bson import json_util as json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CallbackContext
from handlers.misc import handle_closing_action
from utils.actions import Actions
from utils.data.reminders import set_on_last_reminder, get_reminders, add_reminder, remove_reminder
from utils.data.meds import get_meds
from utils.data.user_data import get_timezone
from utils.helpers.misc import answer_callback_query, get_user_id
from utils.l10n import t


def show_reminders(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    reminders = get_reminders(user_id)
    timezone = get_timezone(user_id)

    if not timezone:
        handle_closing_action(update, context, Actions.ADD_TIMEZONE)
        return

    text = ""
    keyboard = [
        [InlineKeyboardButton(
                text=t(Actions.ADD_REMINDER, user_id),
                callback_data=json.dumps({
                    "action": Actions.ADD_REMINDER
                })
            )]
    ]
    
    if reminders:
        reminder_list = "\n".join(\
            f"{i+1}. {reminder.meds.name} {reminder.dosage}\
{(' ' + t('with food', user_id)) if reminder.with_food else ''} \
{t('at', user_id)} {str(reminder.time.hour + timezone).zfill(2)}:{str(reminder.time.minute).zfill(2)}" \
            for i, reminder in enumerate(reminders))

        text = \
f"""{t('Your timed reminders:', user_id)}

{reminder_list}"""

        keyboard[0] += [InlineKeyboardButton(
            text=t(Actions.REMOVE_REMINDER, user_id),
            callback_data=json.dumps({
                "action": Actions.REMOVE_REMINDER
            })
        )]
    else:
        text = t("You have no timed reminders right now.", user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_reminder_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    meds = get_meds(user_id)

    text = t(Actions.ADD_REMINDER_SET_MEDS, user_id)
    keyboard = [
        [InlineKeyboardButton(
            text=med.name,
            callback_data=json.dumps({
                "action": Actions.ADD_REMINDER_SET_MEDS,
                "meds._id": med._id
            })
        ) for med in meds]
    ]

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))

@answer_callback_query
def add_reminder_set_meds(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    add_reminder(user_id, {"meds": data.get("meds._id")})

    text = t(Actions.ADD_REMINDER_SET_DOSAGE, user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=ForceReply())


def add_reminder_set_dosage(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    dosage = update.message.text
    set_on_last_reminder(user_id, "dosage", dosage)

    text = t(Actions.ADD_REMINDER_SET_WITH_FOOD, user_id)
    keyboard = [
        [InlineKeyboardButton(
            text=t(["No", "Yes"][option], user_id),
            callback_data=json.dumps({
                "action": Actions.ADD_REMINDER_SET_WITH_FOOD,
                "with_food": option
            })
        ) for option in [True, False]]
    ]

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_reminder_set_with_food(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    set_on_last_reminder(user_id, "with_food", data.get("with_food"))

    text = t(Actions.ADD_REMINDER_SET_TIME, user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=ForceReply())


def add_reminder_set_time(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    timezone = get_timezone(user_id)
    [hour, minute] = [int(part) for part in update.message.text.split(":")]
    time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(hours=timezone)
    set_on_last_reminder(user_id, "time", time)

    handle_closing_action(update, context, Actions.DONE)

    show_reminders(update, context)


@answer_callback_query
def remove_reminder_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    reminders = get_reminders(user_id)

    text = t(Actions.REMOVE_REMINDER_SET_ID, user_id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
                text=reminder.meds.name,
                callback_data=json.dumps({
                    "action": Actions.REMOVE_REMINDER_SET_ID,
                    "_id": reminder._id
                })
            ) for reminder in reminders]
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


@answer_callback_query
def remove_reminder_set_id(update: Update, context: CallbackContext):
    remove_reminder(json.loads(update.callback_query.data).get("_id"))

    handle_closing_action(update, context, Actions.DONE)

    show_reminders(update, context)
