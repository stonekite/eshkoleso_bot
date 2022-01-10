from datetime import datetime
from .client import client
from typing import Union
from utils.helpers.misc import is_archived
from bson.objectid import ObjectId


class Question():
    def __init__(self, question: Union[dict, ObjectId]):
        if not question:
            question = {}
        elif isinstance(question, ObjectId):
            question = get_question(question).__dict__
        

        self._id: ObjectId = question.get("_id", None)
        self.text: str = question.get("text", "")
        self.answers: list[Answer] = [Answer(answer) for answer in question.get("answers", [])]
        self.is_archived: bool = question.get("is_archived", False)


class Answer():
    def __init__(self, answer: dict):
        if not answer:
            answer = {}
        
        self.text: str = answer.get("text", "")
        self.date: datetime = answer.get("date", None)


def get_all_questions(user_id: int) -> list[Question]:
    questions = client.find_one({
        "_id": user_id
    }, {
        "_id": 0,
        "journal_questions": 1
    }).get(
        "journal_questions",
        []
    )

    return [Question(question) for question in questions]


def get_questions(user_id: int) -> list[Question]:
    return [questions for questions in get_all_questions(user_id) if not is_archived(questions)]


def get_question(questions_id: ObjectId):
    questions = client.find_one({
        "journal_questions._id": questions_id
    }, {
        "_id": 0,
        "journal_questions": 1
    }).get(
        "journal_questions",
        []
    )
    if not questions:
        questions = [{}]

    return Question(questions[0])


def add_question(user_id: int, question: Question):
    question["_id"] = ObjectId()
    client.update_one({
        "_id": user_id,
    }, {
        "$push": {
            "journal_questions": question
        }
    })


def remove_question(questions_id: ObjectId):
    client.update_one({
        "journal_questions._id": questions_id,
    }, {
        "$set": {
            "journal_questions.$.is_archived": True
        }
    })


def add_answer(question_id: ObjectId, text: str):    
    client.update_one({
        "journal_questions._id": question_id,
    }, {
        "$push": {
            "journal_questions.$.answers": {
                "date": datetime.utcnow(),
                "text": text
            }
        }
    })
