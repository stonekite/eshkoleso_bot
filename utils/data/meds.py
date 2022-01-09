from .client import client
from typing import Union
from utils.helpers.misc import is_archived
from bson.objectid import ObjectId


class Med():
    def __init__(self, med: Union[dict, ObjectId]):
        if not med:
            med = {}
        elif isinstance(med, ObjectId):
            med = get_med(med).__dict__
        

        self._id: ObjectId = med.get("_id", None)
        self.name: str = med.get("name", "")
        self.is_archived: bool = med.get("is_archived", False)


def get_all_meds(user_id: int) -> list[Med]:
    meds = client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "meds": 1
    }).get(
        "meds",
        []
    )

    return [Med(med) for med in meds]


def get_meds(user_id: int) -> list[Med]:
    return [meds for meds in get_all_meds(user_id) if not is_archived(meds)]


def get_med(meds_id: ObjectId):
    meds = client.find_one({
        "meds._id": meds_id
    }, {
        "_id": 0,
        "meds": 1
    }).get(
        "meds",
        []
    )
    if not meds:
        meds = [{}]

    return Med(meds[0])


def add_meds(user_id: int, med: Med):
    med["_id"] = ObjectId()
    client.update_one({
        "_id": user_id,
    }, {
        "$push": {
            "meds": med
        }
    })


def remove_meds(meds_id: ObjectId):
    client.update_one({
        "meds._id": meds_id,
    }, {
        "$set": {
            "meds.$.is_archived": True
        }
    })
