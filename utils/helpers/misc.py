from typing import Callable
from telegram import Update
from telegram.ext.callbackcontext import CallbackContext


def get_user_id(update: Update) -> int:
    return (update.message or update.callback_query).from_user.id


def answer_callback_query(function: Callable):
    def inner(update: Update, context: CallbackContext, *args, **kwargs):
        function(update, context, *args, **kwargs)

        if update.callback_query:
            context.bot.answer_callback_query(update.callback_query.id)
    
    return inner
