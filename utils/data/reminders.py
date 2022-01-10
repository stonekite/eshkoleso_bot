from typing import Any, Union
from .client import client
from utils.helpers.misc import is_archived
from .meds import Med
from bson.objectid import ObjectId
from datetime import time


class Reminder():
    def __init__(self, reminder: Union[dict, ObjectId]):
        if not reminder:
            reminder = {}
        elif isinstance(reminder, ObjectId):
            reminder = get_reminder(reminder).__dict__

        self._id: ObjectId = reminder.get("_id", None)
        self.meds: Med = Med(reminder.get("meds", {}))
        self.dosage: str = reminder.get("dosage", "")
        self.with_food: bool = reminder.get("with_food", False)
        self.time: time = reminder.get("time", None)
        self.is_archived: bool = reminder.get("is_archived", False)


def get_all_reminders(user_id: int) -> list[Reminder]:
    reminders = client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "reminders": 1
    }).get(
        "reminders",
        []
    )

    return [Reminder(reminder) for reminder in reminders]


def get_reminders(user_id: int) -> list[Reminder]:
    return [reminder for reminder in get_all_reminders(user_id) if not is_archived(reminder)]


def get_reminder(reminder_id: ObjectId):
    reminder = client.find_one({
        "reminders._id": reminder_id
    }, {
        "_id": 0,
        "reminders": 1
    }).get(
        "reminders",
        []
    )
    if not reminder:
        reminder = [{}]

    return Reminder(reminder[0])


def add_reminder(user_id: int, reminder: Reminder):
    reminder["_id"] = ObjectId()
    client.update_one({
        "_id": user_id
    }, {
        "$push": {
            "reminders": reminder
        }
    })


def set_on_last_reminder(user_id: int, key: str, value: Any):
    last_reminder_id = get_reminders(user_id)[-1]._id
    client.update_one({
        "reminders._id": last_reminder_id
    }, {
        "$set": {
            f"reminders.$.{key}": value
        }
    })


def remove_reminder(reminder_id: ObjectId):
    client.update_one({
        "reminders._id": reminder_id
    }, {
        "$set": {
            "reminders.$.is_archived": True
        }
    })
