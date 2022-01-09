from typing import Callable, Union
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext


def get_user_id(update: Update) -> int:
    return (update.message or update.callback_query).from_user.id


def answer_callback_query(function: Callable) -> Callable:
    def inner(update: Update, context: CallbackContext, *args, **kwargs):
        function(update, context, *args, **kwargs)
        if update.callback_query:
            context.bot.answer_callback_query(update.callback_query.id)
    
    return inner


def remove_last_message_after(function: Callable) -> Callable:
    def inner(update: Update, *args, **kwargs):
        function(update, *args, **kwargs)
        if update.message and update.message.reply_to_message:
            update.message.reply_to_message.delete()
        elif update.callback_query and update.callback_query.message:
            update.callback_query.message.delete()

    return inner


def is_archived(entity: Union[dict, object]) -> bool:
    if not isinstance(entity, dict):
        entity = entity.__dict__

    return "is_archived" in entity and entity["is_archived"] == True
