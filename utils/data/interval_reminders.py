from typing import Any, Union
from .client import client
from utils.helpers.misc import is_archived
from .meds import Med
from bson.objectid import ObjectId


class IntervalReminder():
    def __init__(self, reminder: Union[dict, ObjectId]):
        if not reminder:
            reminder = {}
        elif isinstance(reminder, ObjectId):
            reminder = get_interval_reminder(reminder).__dict__

        self._id: ObjectId = reminder.get("_id", None)
        self.meds: Med = Med(reminder.get("meds", {}))
        self.dosage: str = reminder.get("dosage", "")
        self.with_food: bool = reminder.get("with_food", False)
        self.repetitions: int = reminder.get("repetitions", 0)
        self.interval: int = reminder.get("interval", 0)
        self.is_archived: bool = reminder.get("is_archived", False)


def get_all_interval_reminders(user_id: int) -> list[IntervalReminder]:
    reminders = client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "interval_reminders": 1
    }).get(
        "interval_reminders",
        []
    )

    return [IntervalReminder(reminder) for reminder in reminders]


def get_interval_reminders(user_id: int) -> list[IntervalReminder]:
    return [reminder for reminder in get_all_interval_reminders(user_id) if not is_archived(reminder)]

def get_interval_reminder(reminder_id: ObjectId):
    reminder = client.find_one({
        "interval_reminders._id": reminder_id
    }, {
        "_id": 0,
        "interval_reminders": 1
    }).get(
        "interval_reminders",
        []
    )
    if not reminder:
        reminder = [{}]

    return IntervalReminder(reminder[0])


def add_interval_reminder(user_id: int, reminder: IntervalReminder):
    reminder["_id"] = ObjectId()
    client.update_one({
        "_id": user_id
    }, {
        "$push": {
            "interval_reminders": reminder
        }
    })


def set_on_last_interval_reminder(user_id: int, key: str, value: Any):
    last_reminder_id = get_interval_reminders(user_id)[-1]._id
    client.update_one({
        "interval_reminders._id": last_reminder_id
    }, {
        "$set": {
            f"interval_reminders.$.{key}": value
        }
    })


def remove_interval_reminder(reminder_id: ObjectId):
    client.update_one({
        "interval_reminders._id": reminder_id
    }, {
        "$set": {
            "interval_reminders.$.is_archived": True
        }
    })
