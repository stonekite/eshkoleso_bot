from bson import json_util as json
from telegram import Update
from telegram.ext import CallbackContext
from utils.actions import Actions, action_messages
from utils.l10n import is_in_translation_keys, matching_key
from .meds import show_meds, add_meds_start, add_meds_set_name, remove_meds_start, remove_meds_set_id
from .interval_reminders import show_interval_reminders, add_interval_reminder_start, remove_interval_reminder, start_interval_reminders
from .misc import handle_closing_action


action_handlers = dict({
    Actions.SHOW_MEDS: show_meds,
    Actions.ADD_MEDS: add_meds_start,
    Actions.ADD_MEDS_SET_NAME: add_meds_set_name,
    Actions.REMOVE_MEDS: remove_meds_start,
    Actions.REMOVE_MEDS_SET_ID: remove_meds_set_id,
    Actions.SHOW_INTERVAL_REMINDERS: show_interval_reminders,
    Actions.ADD_INTERVAL_REMINDER: add_interval_reminder_start,
    Actions.REMOVE_INTERVAL_REMINDER: remove_interval_reminder,
    Actions.START_INTERVAL_REMINDERS: start_interval_reminders,
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
