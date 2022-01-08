from bson import json_util as json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CallbackContext
from handlers.misc import handle_closing_action
from utils.actions import Actions
from utils.data.meds import get_meds, add_meds, remove_meds
from utils.helpers.misc import get_user_id, answer_callback_query
from utils.l10n import t


def show_meds(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    meds = get_meds(user_id)

    text = ""
    keyboard = [
        [
            InlineKeyboardButton(
                text=t(Actions.ADD_MEDS, user_id),
                callback_data=json.dumps({
                    "action": Actions.ADD_MEDS
                })
            )
        ]
    ]

    if meds:
        meds_list = "\n".join(f"{i+1}. {med.name}" for i, med in enumerate(meds))

        text = \
f"""{t('Your meds:', user_id)}

{meds_list}"""

        keyboard[0] += [InlineKeyboardButton(
            text=t(Actions.REMOVE_MEDS, user_id),
            callback_data=json.dumps({
                "action": Actions.REMOVE_MEDS
            })
        )]
    else:
        text = t("You have no meds right now.", user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_meds_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    text = t(Actions.ADD_MEDS_SET_NAME, user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=ForceReply())


def add_meds_set_name(update: Update, context: CallbackContext):
    user_id = get_user_id(update)

    add_meds(user_id, {"name": update.message.text})

    handle_closing_action(update, context, Actions.DONE)

    show_meds(update, context)


@answer_callback_query
def remove_meds_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    meds = get_meds(user_id)

    text = t(Actions.REMOVE_MEDS_SET_ID, user_id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text=med.name,
                callback_data=json.dumps({
                    "action": Actions.REMOVE_MEDS_SET_ID,
                    "_id": med._id
                })
            ) for med in meds
        ]
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


@answer_callback_query
def remove_meds_set_id(update: Update, context: CallbackContext):
    remove_meds(json.loads(update.callback_query.data).get("_id"))

    handle_closing_action(update, context, Actions.DONE)

    show_meds(update, context)
