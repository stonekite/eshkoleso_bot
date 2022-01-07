import itertools
from typing import Union
from .data.user_data import get_language
from .actions import Actions, action_messages


translations = dict({
    "ru": dict({
        "Welcome!": "Добро пожаловать!",
        "Done!": "Готово!",

        "My meds": "Мои препараты",
        "Add meds": "Добавить препарат",
        "Remove meds": "Удалить препарат",
        "Please enter the name of the meds.": "Пожалуйста, введите название препарата.",
        "Please select the meds you want to remove.": "Пожалуйста, выберите препарат, который вы хотите удалить.",

        "My journal": "Моя анкета",
        "Add question": "Добавить вопрос",
        "Remove question": "Удалить вопрос",
        "Add answer": "Добавить ответ",

        "My timed reminders": "Мои напоминания по времени",
        "Add reminder": "Добавить напоминание",
        "Remove reminder": "Удалить напоминание",

        "My interval reminders": "Мои напоминания с интервалом",
        "Start interval reminders": "Начать напоминания с интервалом",

        "Sorry, something went wrong.": "Извините, что-то пошло не так.",
        "Sorry, I didn't get that.": "Извините, я не понял."
    })
})

translation_keys = []
for translation in translations.values():
    translation_keys += translation.keys()
translation_keys = set(translation_keys)


def t(text: Union[str, Actions], user_id: int) -> str:
    language = get_language(user_id)
    if type(text) == Actions:
        text = action_messages[text]
    return text if language == "en" else translations.get(language, {}).get(text, text)


def t_get_all_options(text: str) -> list[str]:
    return list(set(text, ([translation for translation in language.get(text, text)] for language in translations.values())))


def is_in_translation_keys(text: str):
    return text in translation_keys


def matching_key(text: str):
    for translation in translations.values():
        for item in translation.items():
            if item[1] == text:
                return item[0]
