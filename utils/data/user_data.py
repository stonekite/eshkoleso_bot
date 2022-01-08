from datetime import date
from utils.data.meds import Med
from utils.data.reminders import Reminder
from utils.data.interval_reminders import IntervalReminder
from utils.helpers.misc import is_archived
from .client import client


class UserData():
    def __init__(self, user_data: dict):
        user_data = user_data if user_data else {}

        self._id: int = user_data.get("_id", None)
        meds = user_data.get("meds", [])
        self.meds: list[Med] = [Med(med) for med in meds if not is_archived(med)]
        reminders = user_data.get("reminders", [])
        self.reminders: list[Reminder] = [Reminder(reminder) for reminder in reminders if not is_archived(reminder)]
        interval_reminders = user_data.get("interval_reminders", [])
        self.interval_reminders: list[IntervalReminder] = \
            [IntervalReminder(reminder) for reminder in interval_reminders if not is_archived(reminder)]
        self.last_interval_reminder_start_date: date = user_data.get("last_interval_reminder_start_date", None)
        self.language: str = user_data.get("language", "ru")
        self.timezone: int = user_data.get("timezone", None)
        self.is_archived: bool = user_data.get("is_archived", False)


def get_user_data(user_id: int):
    user_data = client.find_one({
        "_id": user_id
    })

    return UserData(user_data)


def ensure_user_exists(user_id: int):
    user_data = client.find_one({
        "_id": user_id
    })

    if not user_data:
        client.insert_one({
            "_id": user_id,
            "language": "ru"
        })


def get_language(user_id: int):
    return client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "language": 1
    }).get(
        "language",
        "ru"
    )


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


def timezone_is_set(user_id: int) -> bool:
    return bool(get_timezone(user_id))
