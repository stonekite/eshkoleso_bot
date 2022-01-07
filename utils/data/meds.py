from .client import client
from .user_data import get_user_data


def get_meds(user_id: int) -> list[str]:
    return get_user_data(user_id).get("meds", [])


def add_meds(user_id: int, name: str) -> str:
    client.update_one({
        "_id": user_id,
    }, {
        "$push": {
            "meds": dict({
                "name": name
            })
        }
    })


def remove_meds(user_id: int, index: int) -> str:
    client.update_one({
        "_id": user_id,
    }, {
        "$set": {
            f"meds.{index}": {
                "name": "REMOVE"
            }
        }
    })
    client.update_one({
        "_id": user_id
    }, {
        "$pull": {
            "meds": {
                "name": "REMOVE"
            }
        }
    })
