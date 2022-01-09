from bson import json_util as json
from telegram import Update
from telegram.ext import CallbackContext

from .journal import add_journal_time, add_question_set_text, add_question_start, remove_question_set_id, remove_question_start, show_questions, add_answer
from .scheduler import schedule_interval_reminders, stop_job
from .reminders import add_reminder_set_dosage, add_reminder_set_meds, add_reminder_set_time, add_reminder_set_with_food, add_reminder_start, remove_reminder_set_id, remove_reminder_start, show_reminders
from utils.actions import Actions, action_messages
from utils.l10n import is_in_translation_keys, matching_key
from .meds import show_meds, add_meds_start, add_meds_set_name, remove_meds_start, remove_meds_set_id
from .interval_reminders import add_interval_reminder_set_dosage, add_interval_reminder_set_interval, add_interval_reminder_set_meds, add_interval_reminder_set_repetitions, add_interval_reminder_set_with_food, remove_interval_reminder_set_id, show_interval_reminders, add_interval_reminder_start, remove_interval_reminder_start
from .misc import handle_closing_action, add_timezone


action_handlers = dict({
    Actions.SHOW_MEDS: show_meds,
    Actions.ADD_MEDS: add_meds_start,
    Actions.ADD_MEDS_SET_NAME: add_meds_set_name,
    Actions.REMOVE_MEDS: remove_meds_start,
    Actions.REMOVE_MEDS_SET_ID: remove_meds_set_id,
    Actions.SHOW_JOURNAL_QUESTIONS: show_questions,
    Actions.ADD_JOURNAL_QUESTION: add_question_start,
    Actions.ADD_JOURNAL_QUESTION_SET_TEXT: add_question_set_text,
    Actions.REMOVE_JOURNAL_QUESTION: remove_question_start,
    Actions.REMOVE_JOURNAL_QUESTION_SET_ID: remove_question_set_id,
    Actions.ADD_JOURNAL_ANSWER: add_answer,
    Actions.ADD_JOURNAL_TIME: add_journal_time,
    Actions.SHOW_REMINDERS: show_reminders,
    Actions.ADD_REMINDER: add_reminder_start,
    Actions.ADD_REMINDER_SET_MEDS: add_reminder_set_meds,
    Actions.ADD_REMINDER_SET_DOSAGE: add_reminder_set_dosage,
    Actions.ADD_REMINDER_SET_WITH_FOOD: add_reminder_set_with_food,
    Actions.ADD_REMINDER_SET_TIME: add_reminder_set_time,
    Actions.REMOVE_REMINDER: remove_reminder_start,
    Actions.REMOVE_REMINDER_SET_ID: remove_reminder_set_id,
    Actions.SHOW_INTERVAL_REMINDERS: show_interval_reminders,
    Actions.ADD_INTERVAL_REMINDER: add_interval_reminder_start,
    Actions.ADD_INTERVAL_REMINDER_SET_MEDS: add_interval_reminder_set_meds,
    Actions.ADD_INTERVAL_REMINDER_SET_DOSAGE: add_interval_reminder_set_dosage,
    Actions.ADD_INTERVAL_REMINDER_SET_WITH_FOOD: add_interval_reminder_set_with_food,
    Actions.ADD_INTERVAL_REMINDER_SET_REPETITIONS: add_interval_reminder_set_repetitions,
    Actions.ADD_INTERVAL_REMINDER_SET_INTERVAL: add_interval_reminder_set_interval,
    Actions.REMOVE_INTERVAL_REMINDER: remove_interval_reminder_start,
    Actions.REMOVE_INTERVAL_REMINDER_SET_ID: remove_interval_reminder_set_id,
    Actions.START_INTERVAL_REMINDERS: schedule_interval_reminders,
    Actions.ADD_TIMEZONE: add_timezone,
    Actions.STOP_JOB: stop_job,
    Actions.ERROR: lambda update, context: handle_closing_action(update, context, Actions.ERROR),
    Actions.USER_ERROR: lambda update, context: handle_closing_action(update, context, Actions.USER_ERROR)
})


def handle_action(update: Update, context: CallbackContext, action: Actions):
    action_handlers[action](update, context)


def callback_handler(update: Update, context: CallbackContext):
    data = json.loads(update.callback_query.data)
    action = Actions(data.get("action", Actions.ERROR.value))

    handle_action(update, context, action)


def message_handler(update: Update, context: CallbackContext):
    def find_action_from_text(text: str) -> Actions:
        action_message = text
        if not is_in_translation_keys(text):
            action_message = matching_key(text)
        
        action = Actions.USER_ERROR
        for item in action_messages.items():
            if item[1] == action_message:
                action = item[0]
                break
        
        return action

    text = update.message.text
    action = find_action_from_text(text)

    if action == Actions.USER_ERROR:
        text = update.message.reply_to_message.text
        action = find_action_from_text(text)

    handle_action(update, context, action)
