from utils.helpers.misc import is_archived
from .client import client
from bson.objectid import ObjectId


class Med():
    def __init__(self, med: dict):
        med = med if med else {}

        self._id: ObjectId = med.get("_id", None)
        self.name: str = med.get("name", "")
        self.is_archived: bool = med.get("is_archived", False)


def get_meds(user_id: int) -> list[Med]:
    meds = client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "meds": 1
    }).get(
        "meds",
        []
    )

    return [Med(med) for med in meds if not is_archived(med)]


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
