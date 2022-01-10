from datetime import datetime, timedelta
from bson import json_util as json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import JobQueue, CallbackContext
from telegram.update import Update
from handlers.misc import handle_closing_action
from utils.data.journal import get_questions
from utils.updater import updater
from utils.actions import Actions
from utils.data.reminders import Reminder
from utils.data.user_data import UserData, get_all_user_data, get_chat_id, get_last_reminder_message_id, get_user_data, set_last_interval_reminders_start_date, set_last_reminder_message_id
from utils.helpers.misc import answer_callback_query, get_user_id
from utils.l10n import t


queue = JobQueue()
queue.set_dispatcher(updater.dispatcher)
queue.start()


def run_meal_reminder(context: CallbackContext):
    user_id = context.job.context.get("user_id", None)
    text = t("⏰ Time to get some food! You're taking your meds in 30 minutes.", user_id)
    chat_id = get_chat_id(user_id)

    context.bot.send_message(text=text, chat_id=chat_id)


def run_reminder(context: CallbackContext):
    data = context.job.context
    name = data.get("name")
    user_id = data.get("user_id")
    reminder = data.get("reminder")
    chat_id = get_chat_id(user_id)

    last_message_id = get_last_reminder_message_id(user_id)
    if last_message_id:
        context.bot.delete_message(chat_id, last_message_id)

    text = f"⏰ {reminder.meds.name} {reminder.dosage}"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text="✔️",
            callback_data=json.dumps({
                "action": Actions.STOP_JOB,
                "name": name
            })
        )]
    ])

    message = context.bot.send_message(text=text, chat_id=chat_id, reply_markup=keyboard)
    set_last_reminder_message_id(user_id, message.message_id)

    queue.run_once(
        name=name,
        callback=run_reminder,
        when=timedelta(minutes=15),
        context=data
    )


def schedule_reminder(user: UserData, reminder: Reminder):
    name = f"reminder.{reminder._id}"
    when = datetime.utcnow().replace(hour=reminder.time.hour, minute=reminder.time.minute, second=0, microsecond=0)

    queue.run_once(
        name=name,
        callback=run_reminder,
        when=when,
        context={
            "user_id": user._id,
            "reminder": reminder,
            "name": name
        }
    )

    if reminder.with_food:
        queue.run_once(
            name=f"meal_reminder.{reminder._id}",
            callback=run_meal_reminder,
            when=when - timedelta(minutes=30),
            context={
                "user_id": user._id
            }
        )


def schedule_reminders(users: list[UserData]):
    for user in users:
        for reminder in user.reminders:
            schedule_reminder(user, reminder)


def schedule_interval_reminders(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    user = get_user_data(user_id)

    times = []

    for reminder in user.interval_reminders:
        now = datetime.utcnow()
        for i in range(1, reminder.repetitions):
            time = now + timedelta(hours=i * reminder.interval)
            times += [time]
            schedule_reminder(user, Reminder({
                "_id": str(reminder._id) + "." + str(i),
                "meds": reminder.meds,
                "dosage": reminder.dosage,
                "with_food": reminder.with_food,
                "time": time,
            }))
    
    set_last_interval_reminders_start_date(user_id, datetime.utcnow())

    handle_closing_action(update, context, \
        t("Reminders scheduled for", user_id) + \
            " " + ", ".join(str(time.hour + user.timezone).zfill(2) + ":" + str(time.minute).zfill(2) for time in times))


def run_journal(context: CallbackContext):
    data = context.job.context
    name = data.get("name", "")
    user_id = data.get("user_id", None)
    questions = get_questions(user_id)
    chat_id = get_chat_id(user_id)

    last_message_id = get_last_reminder_message_id(user_id)
    if last_message_id:
        context.bot.delete_message(chat_id, last_message_id)

    text = questions[0].text
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(
            text=i,
            callback_data=json.dumps({
                "action": Actions.ADD_JOURNAL_ANSWER,
                "current_question_index": 0,
                "answer": i
            })
        ) for i in range(1, 6)]
    ])

    message = context.bot.send_message(text=text, chat_id=chat_id, reply_markup=keyboard)
    set_last_reminder_message_id(user_id, message.message_id)

    queue.run_once(
        name=name,
        callback=run_journal,
        when=timedelta(minutes=30),
        context=data
    )


def schedule_journals(users: list[UserData]):
    now = datetime.utcnow()
    for user in users:
        if user.journal_questions:
            name = f"journal.{user._id}"
            when = now.replace(hour=user.journal_time.hour, minute=user.journal_time.minute, second=0, microsecond=0)
            queue.run_once(
                name=name,
                callback=run_journal,
                when=when,
                context={
                    "name": name,
                    "user_id": user._id,
                    "questions": user.journal_questions
                }
            )


def schedule_actions(context: CallbackContext=None):
    users = get_all_user_data()
    schedule_reminders(users)
    schedule_journals(users)

    now = datetime.utcnow()
    when = datetime(now.year, now.month, now.day + 1)

    queue.run_once(
        name="scheduler",
        callback=schedule_actions,
        when=when
    )

    print([job.name for job in queue.jobs()])


@answer_callback_query
def stop_job(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    data = json.loads(update.callback_query.data)
    name = data.get("name", "")

    jobs = queue.get_jobs_by_name(name)
    for job in jobs:
        job.remove()
    
    set_last_reminder_message_id(user_id, None)

    handle_closing_action(update, context, Actions.DONE)
