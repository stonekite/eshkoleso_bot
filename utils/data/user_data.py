from .client import client


def get_user_data(user_id: int):
    return client.find_one({
        "_id": user_id
    })


def ensure_user_exists(user_id: int):
    user_data = get_user_data(user_id)
    if not user_data:
        client.insert_one({
            "_id": user_id,
            "language": "ru"
        })


def get_language(user_id: int):
    return get_user_data(user_id).get("language", "ru")


def set_language(user_id: int, language: str):
    client.update_one({
        "_id": user_id
    }, {
        "$set": {
            "language": language
        }
    })
