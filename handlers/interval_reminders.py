from bson import json_util as json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CallbackContext
from handlers.misc import handle_closing_action
from handlers.scheduler import schedule_interval_reminders
from utils.actions import Actions
from utils.data.interval_reminders import set_on_last_interval_reminder, get_interval_reminders, add_interval_reminder, remove_interval_reminder
from utils.data.meds import get_meds
from utils.helpers.misc import answer_callback_query, get_user_id
from utils.l10n import t


def show_interval_reminders(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    reminders = get_interval_reminders(user_id)

    text = ""
    keyboard = [
        [InlineKeyboardButton(
            text=t(Actions.ADD_INTERVAL_REMINDER, user_id),
            callback_data=json.dumps({
                "action": Actions.ADD_INTERVAL_REMINDER
            })
        )]
    ]
    
    if reminders:
        reminder_list = "\n".join(\
            f"{i+1}. {reminder.meds.name} {reminder.dosage}\
{(' ' + t('with food', user_id)) if reminder.with_food else ''}, \
{reminder.repetitions} {t('times', user_id)} {t('every', user_id)} {reminder.interval} {t('hours', user_id)}" \
            for i, reminder in enumerate(reminders))

        text = \
f"""{t('Your interval reminders:', user_id)}

{reminder_list}"""

        keyboard[0] += [InlineKeyboardButton(
            text=t(Actions.REMOVE_INTERVAL_REMINDER, user_id),
            callback_data=json.dumps({
                "action": Actions.REMOVE_INTERVAL_REMINDER
            })
        )]
    else:
        text = t("You have no interval reminders right now.", user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_interval_reminder_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    meds = get_meds(user_id)

    text = t(Actions.ADD_INTERVAL_REMINDER_SET_MEDS, user_id)
    keyboard = [
        [InlineKeyboardButton(
            text=med.name,
            callback_data=json.dumps({
                "action": Actions.ADD_INTERVAL_REMINDER_SET_MEDS,
                "meds._id": med._id
            })
        ) for med in meds]
    ]

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))

@answer_callback_query
def add_interval_reminder_set_meds(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    add_interval_reminder(user_id, {"meds": data.get("meds._id")})

    text = t(Actions.ADD_INTERVAL_REMINDER_SET_DOSAGE, user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=ForceReply())


def add_interval_reminder_set_dosage(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    dosage = update.message.text
    set_on_last_interval_reminder(user_id, "dosage", dosage)

    text = t(Actions.ADD_INTERVAL_REMINDER_SET_WITH_FOOD, user_id)
    keyboard = [
        [InlineKeyboardButton(
            text=t(["No", "Yes"][option], user_id),
            callback_data=json.dumps({
                "action": Actions.ADD_INTERVAL_REMINDER_SET_WITH_FOOD,
                "with_food": option
            })
        ) for option in [True, False]]
    ]

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_interval_reminder_set_with_food(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    set_on_last_interval_reminder(user_id, "with_food", data.get("with_food"))

    text = t(Actions.ADD_INTERVAL_REMINDER_SET_REPETITIONS, user_id)
    keyboard = [
        [InlineKeyboardButton(
            text=option,
            callback_data=json.dumps({
                "action": Actions.ADD_INTERVAL_REMINDER_SET_REPETITIONS,
                "repetitions": option
            })
        ) for option in range(2, 10)]
    ]

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_interval_reminder_set_repetitions(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    repetitions = data.get("repetitions")
    set_on_last_interval_reminder(user_id, "repetitions", repetitions)

    text = t(Actions.ADD_INTERVAL_REMINDER_SET_INTERVAL, user_id)
    keyboard = [
        [InlineKeyboardButton(
            text=option,
            callback_data=json.dumps({
                "action": Actions.ADD_INTERVAL_REMINDER_SET_INTERVAL,
                "interval": option
            })
        ) for option in range(2, 10) if (repetitions - 1) * option < 24]
    ]

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_interval_reminder_set_interval(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    set_on_last_interval_reminder(user_id, "interval", data.get("interval"))

    handle_closing_action(update, context, Actions.DONE)
    
    show_interval_reminders(update, context)


@answer_callback_query
def remove_interval_reminder_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    reminders = get_interval_reminders(user_id)

    text = t(Actions.REMOVE_INTERVAL_REMINDER_SET_ID, user_id)

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=reminder.meds.name,
            callback_data=json.dumps({
                "action": Actions.REMOVE_INTERVAL_REMINDER_SET_ID,
                "_id": reminder._id
            })
        ) for reminder in reminders]
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


@answer_callback_query
def remove_interval_reminder_set_id(update: Update, context: CallbackContext):
    remove_interval_reminder(json.loads(update.callback_query.data).get("_id"))

    handle_closing_action(update, context, Actions.DONE)

    show_interval_reminders(update, context)
