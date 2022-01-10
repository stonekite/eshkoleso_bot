from datetime import datetime, timedelta
from utils.data.journal import Question
from utils.data.meds import Med
from utils.data.reminders import Reminder
from utils.data.interval_reminders import IntervalReminder
from utils.helpers.misc import is_archived
from .client import client


class UserData():
    def __init__(self, user_data: dict):
        user_data = user_data if user_data else {}

        self._id: int = user_data.get("_id", None)
        self.chat_id: int = user_data.get("chat_id", None)
        meds = user_data.get("meds", [])
        self.meds: list[Med] = [Med(med) for med in meds if not is_archived(med)]
        questions = user_data.get("journal_questions", [])
        self.journal_questions: list[Question] = [Question(question) for question in questions if not is_archived(question)]
        self.journal_time: datetime = user_data.get("journal_time", None)
        reminders = user_data.get("reminders", [])
        self.reminders: list[Reminder] = [Reminder(reminder) for reminder in reminders if not is_archived(reminder)]
        interval_reminders = user_data.get("interval_reminders", [])
        self.interval_reminders: list[IntervalReminder] = \
            [IntervalReminder(reminder) for reminder in interval_reminders if not is_archived(reminder)]
        self.last_interval_reminders_start_date: datetime = user_data.get("last_interval_reminders_start_date", None)
        self.language: str = user_data.get("language", "ru")
        self.timezone: int = user_data.get("timezone", None)
        self.is_archived: bool = user_data.get("is_archived", False)


def get_user_data(user_id: int):
    user_data = client.find_one({
        "_id": user_id
    })

    return UserData(user_data)


def get_all_user_data() -> list[UserData]:
    user_data = client.find({})

    return [UserData(user) for user in user_data if not is_archived(user)]


def get_chat_id(user_id: int) -> int:
    return client.find_one({
        "_id": user_id,
    }, {
        "_id": 0,
        "chat_id": 1
    }).get(
        "chat_id",
        None
    )


def ensure_user_exists(user_id: int, chat_id: int):
    user_data = client.find_one({
        "_id": user_id
    })
    
    if not user_data:
        client.insert_one({
            "_id": user_id,
            "chat_id": chat_id,
            "language": "ru"
        })


stored_languages = dict()


def get_language(user_id: int) -> str:
    now = datetime.utcnow()
    if user_id not in stored_languages or (now - stored_languages[user_id]["time"]) < timedelta(hours=1):
        language = client.find_one({
            "_id": user_id
        }, {
            "_id": 0,
            "language": 1
        }).get(
            "language",
            "ru"
        )

        stored_languages[user_id] = dict({
            "language": language,
            "time": now
        })

    return stored_languages[user_id]["language"]


def set_language(user_id: int, language: str):
    client.update_one({
        "_id": user_id
    }, {
        "$set": {
            "language": language
        }
    })


def get_timezone(user_id: int) -> int:
    return client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "timezone": 1
    }).get(
        "timezone",
        None
    )


def is_timezone_set(user_id: int) -> bool:
    return isinstance(get_timezone(user_id), int)


def set_timezone(user_id: int, offset: int):
    client.update_one({
        "_id": user_id
    }, {
        "$set": {
            "timezone": int(offset)
        }
    })


def is_journal_time_set(user_id: int) -> bool:
    journal_time = client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "journal_time": 1
    }).get(
        "journal_time",
        None
    )
    
    return isinstance(journal_time, datetime)


def set_journal_time(user_id: int, time: datetime):
    client.update_one({
        "_id": user_id
    }, {
        "$set": {
            "journal_time": time
        }
    })


def set_last_interval_reminders_start_date(user_id: int, date: datetime):
    client.update_one({
        "_id": user_id
    }, {
        "$set": {
            "last_interval_reminders_start_date": date
        }
    })


def get_last_reminder_message_id(user_id: int) -> int:
    return client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "last_reminder_message_id": 1
    }).get(
        "last_reminder_message_id",
        None
    )


def set_last_reminder_message_id(user_id: int, message_id: int):
    client.update_one({
        "_id": user_id
    }, {
        "$set": {
            "last_reminder_message_id": message_id
        }
    })
