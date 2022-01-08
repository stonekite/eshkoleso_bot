from typing import Union
from .data.user_data import get_language
from .actions import Actions, action_messages


translations = dict({
    "ru": dict({
        "Welcome!": "Добро пожаловать!",
        "Your meds:": "Ваши препараты:",
        "You have no meds right now.": "Сейчас у вас нет препаратов.",
        "Your timed reminders:": "Ваши напоминания по времени:",
        "You have no timed reminders right now.": "Сейчас у вас нет напоминаний по времени",
        "Your interval reminders:": "Ваши напоминания с интервалом:",
        "You have no interval reminders right now.": "Сейчас у вас нет напоминаний с интервалом.",
        "times": "раза",
        "every": "каждые",
        "hours": "ч.",

        action_messages[Actions.SHOW_MEDS]: "💊 Мои препараты",
        action_messages[Actions.ADD_MEDS]: "➕ Добавить препарат",
        action_messages[Actions.ADD_MEDS_SET_NAME]: "Пожалуйста, введите название препарата.",
        action_messages[Actions.REMOVE_MEDS]: "❌ Удалить препарат",
        action_messages[Actions.REMOVE_MEDS_SET_ID]: "Пожалуйста, выберите препарат, который вы хотите удалить.",

        action_messages[Actions.SHOW_JOURNAL_QUESTIONS]: "📖 Моя анкета",
        action_messages[Actions.ADD_JOURNAL_QUESTION]: "➕ Добавить вопрос",
        action_messages[Actions.REMOVE_JOURNAL_QUESTION]: "❌ Удалить вопрос",
        action_messages[Actions.ADD_JOURNAL_RESPONSE]: "Добавить ответ",

        action_messages[Actions.SHOW_REMINDERS]: "⏰ Мои напоминания по времени",
        action_messages[Actions.ADD_REMINDER]: "➕ Добавить напоминание",
        action_messages[Actions.REMOVE_REMINDER]: "❌ Удалить напоминание",

        action_messages[Actions.SHOW_INTERVAL_REMINDERS]: "⏰ Мои напоминания с интервалом",
        action_messages[Actions.START_INTERVAL_REMINDERS]: "⏲️ Начать напоминания с интервалом",

        action_messages[Actions.DONE]: "Готово! ✔️",
        action_messages[Actions.ERROR]: "Извините, что-то пошло не так.",
        action_messages[Actions.USER_ERROR]: "Извините, я не понял."
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
