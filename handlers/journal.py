from datetime import datetime, timedelta
from bson import json_util as json
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CallbackContext
from handlers.misc import handle_closing_action
from handlers.scheduler import stop_job
from utils.actions import Actions
from utils.data.journal import get_questions, add_question, remove_question, add_answer as save_answer
from utils.data.user_data import get_timezone, is_journal_time_set, is_timezone_set, set_journal_time
from utils.helpers.misc import get_user_id, answer_callback_query
from utils.l10n import t


def show_questions(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    questions = get_questions(user_id)

    if not is_timezone_set(user_id):
        handle_closing_action(update, context, Actions.ADD_TIMEZONE)
        return

    if not is_journal_time_set(user_id):
        handle_closing_action(update, context, Actions.ADD_JOURNAL_TIME)
        return

    text = ""
    keyboard = [
        [InlineKeyboardButton(
            text=t(Actions.ADD_JOURNAL_QUESTION, user_id),
            callback_data=json.dumps({
                "action": Actions.ADD_JOURNAL_QUESTION
            })
        )]
    ]

    if questions:
        questions_list = "\n".join(f"{i+1}. {question.text}" for i, question in enumerate(questions))

        text = \
f"""{t('Your questions:', user_id)}

{questions_list}"""

        keyboard[0] += [InlineKeyboardButton(
            text=t(Actions.REMOVE_JOURNAL_QUESTION, user_id),
            callback_data=json.dumps({
                "action": Actions.REMOVE_JOURNAL_QUESTION
            })
        )]
    else:
        text = t("Your journal has no questions right now.", user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(keyboard))


@answer_callback_query
def add_question_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    text = t(Actions.ADD_JOURNAL_QUESTION_SET_TEXT, user_id)

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=ForceReply())


def add_question_set_text(update: Update, context: CallbackContext):
    user_id = get_user_id(update)

    add_question(user_id, {"text": update.message.text})

    handle_closing_action(update, context, Actions.DONE)

    show_questions(update, context)


@answer_callback_query
def remove_question_start(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    questions = get_questions(user_id)

    text = t(Actions.REMOVE_JOURNAL_QUESTION_SET_ID, user_id)
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=question.text,
            callback_data=json.dumps({
                "action": Actions.REMOVE_JOURNAL_QUESTION_SET_ID,
                "_id": question._id
            })
        )] for question in questions
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


@answer_callback_query
def remove_question_set_id(update: Update, context: CallbackContext):
    remove_question(json.loads(update.callback_query.data).get("_id"))

    handle_closing_action(update, context, Actions.DONE)

    show_questions(update, context)


@answer_callback_query
def add_answer(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    current_question_index = data.get("current_question_index", None)
    questions = get_questions(user_id)

    if current_question_index == len(questions) - 1:
        stop_job(update, context)
        return

    answer = data.get("answer", "")

    save_answer(questions[current_question_index]._id, answer)

    current_question_index += 1
    data["current_question_index"] = current_question_index

    text = questions[current_question_index].text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=i,
            callback_data=json.dumps(data)
        ) for i in range(1, 6)]
    ])

    context.bot.send_message(text=text, chat_id=update.effective_chat.id, reply_markup=keyboard)


def add_journal_time(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    timezone = get_timezone(user_id)
    [hour, minute] = [int(part) for part in update.message.text.split(":")]
    time = datetime.utcnow().replace(hour=hour, minute=minute, second=0, microsecond=0) - timedelta(hours=timezone)

    set_journal_time(user_id, time)

    handle_closing_action(update, context, Actions.DONE)

    show_questions(update, context)
