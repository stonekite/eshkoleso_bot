import json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CallbackContext
from handlers.misc import handle_closing_action
from utils.actions import Actions
from utils.data.meds import get_meds, add_meds, remove_meds
from utils.helpers.misc import answer_callback_query, get_user_id
from utils.l10n import t


def show_meds(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    meds = get_meds(user_id)
    
    if not meds:
        return

    text_lines = [f"{i+1}. {med.get('name', '')}" for i, med in enumerate(meds)]
    text = "\n".join(text_lines)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=t(Actions.ADD_MEDS, user_id),
                callback_data=json.dumps({
                    "action": Actions.ADD_MEDS
                })
            ),
            InlineKeyboardButton(
                text=t(Actions.REMOVE_MEDS, user_id),
                callback_data=json.dumps({
                    "action": Actions.REMOVE_MEDS
                })
            )
        ]
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


@answer_callback_query
def add_meds_start(update: Update, context: CallbackContext):

    user_id = get_user_id(update)
    text = t(Actions.ADD_MEDS_SET_NAME, user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=ForceReply())


def add_meds_set_name(update: Update, context: CallbackContext):
    user_id = get_user_id(update)

    add_meds(user_id, update.message.text)

    handle_closing_action(update, context, Actions.DONE)

    show_meds(update, context)


@answer_callback_query
def remove_meds_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    meds = get_meds(user_id)

    text = t("Please select the meds you want to remove.", user_id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=med.get("name", ""),
                callback_data=json.dumps({
                    "action": Actions.REMOVE_MEDS_SET_INDEX,
                    "index": i
                })
            ) for i, med in enumerate(meds)
        ]
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


@answer_callback_query
def remove_meds_set_index(update: Update, context: CallbackContext):    
    user_id = get_user_id(update)

    remove_meds(user_id, json.loads(update.callback_query.data).get("index"))

    handle_closing_action(update, context, Actions.DONE)

    show_meds(update, context)
