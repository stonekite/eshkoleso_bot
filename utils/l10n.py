from typing import Union
from .data.user_data import get_language
from .actions import Actions, action_messages


translations = dict({
    "ru": dict({
        "Welcome!": "Добро пожаловать!",
        "Your meds:": "Ваши препараты:",
        "You have no meds right now.": "Сейчас у вас нет препаратов.",
        "Your questions:": "Ваши вопросы:",
        "Your journal has no questions right now.": "Сейчас в вашей анкете нет вопросов.",
        "Please enter the time you want to journal in the format of hh:mm - e.g., 18:00.": \
            "Пожалуйста, введите время, когда вы хотите заполнять анкету, в формате чч:мм - например, 18:00.",
        "Your timed reminders:": "Ваши напоминания по времени:",
        "You have no timed reminders right now.": "Сейчас у вас нет напоминаний по времени.",
        "Your interval reminders:": "Ваши напоминания с интервалом:",
        "You have no interval reminders right now.": "Сейчас у вас нет напоминаний с интервалом.",
        "times": "раза",
        "every": "каждые",
        "hours": "ч.",
        "Yes": "Да",
        "No": "Нет",
        "with food": "с едой",
        "at": "в",
        "⏰ Time to get some food! You're taking your meds in 30 minutes.": \
            "⏰ Пора поесть! Через 30 минут вы принимаете свои препараты.",
        "Reminders scheduled for": "Напоминания запланированы на",

        action_messages[Actions.SHOW_MEDS]: "💊 Мои препараты",
        action_messages[Actions.ADD_MEDS]: "➕ Добавить препарат",
        action_messages[Actions.ADD_MEDS_SET_NAME]: "Пожалуйста, введите название препарата.",
        action_messages[Actions.REMOVE_MEDS]: "❌ Удалить препарат",
        action_messages[Actions.REMOVE_MEDS_SET_ID]: "Пожалуйста, выберите препарат, который вы хотите удалить.",

        action_messages[Actions.SHOW_JOURNAL_QUESTIONS]: "📖 Моя анкета",
        action_messages[Actions.ADD_JOURNAL_QUESTION]: "➕ Добавить вопрос",
        action_messages[Actions.ADD_JOURNAL_QUESTION_SET_TEXT]: "Пожалуйста, введите текст вопроса. Ответами будут цифры от 1 до 5.",
        action_messages[Actions.REMOVE_JOURNAL_QUESTION]: "❌ Удалить вопрос",
        action_messages[Actions.REMOVE_JOURNAL_QUESTION_SET_ID]: "Пожалуйста, выберите вопрос, который вы хотите удалить.",
        action_messages[Actions.ADD_JOURNAL_ANSWER]: "Добавить ответ",

        action_messages[Actions.SHOW_REMINDERS]: "⏰ Мои напоминания по времени",
        action_messages[Actions.ADD_REMINDER]: "➕ Добавить напоминание",
        action_messages[Actions.ADD_REMINDER_SET_DOSAGE]: \
            "Пожалуйста, введите дозировку для этого напоминания по времени - например, количество таблеток.",
        action_messages[Actions.ADD_REMINDER_SET_TIME]: \
            "Пожалуйста, введите время для этого напоминания в формате чч:мм - например, 18:00.",
        action_messages[Actions.REMOVE_REMINDER]: "❌ Удалить напоминание",

        action_messages[Actions.SHOW_INTERVAL_REMINDERS]: "⏰ Мои напоминания с интервалом",
        action_messages[Actions.START_INTERVAL_REMINDERS]: "⏲️ Начать напоминания с интервалом",
        action_messages[Actions.ADD_INTERVAL_REMINDER_SET_MEDS]: "Пожалуйста, выберите препарат.",
        action_messages[Actions.ADD_INTERVAL_REMINDER_SET_DOSAGE]: \
            "Пожалуйста, введите дозировку для этого напоминания с интервалом - например, количество таблеток.",
        action_messages[Actions.ADD_INTERVAL_REMINDER_SET_WITH_FOOD]: \
            "Пожалуйста, выберите, хотите ли вы получать напоминания о еде за 30 минут до приема препарата.",
        action_messages[Actions.ADD_INTERVAL_REMINDER_SET_REPETITIONS]: "Пожалуйста, выберите количество напоминаний в день.",
        action_messages[Actions.ADD_INTERVAL_REMINDER_SET_INTERVAL]: "Пожалуйста, выберите количество часов между напоминаниями.",
        action_messages[Actions.REMOVE_INTERVAL_REMINDER_SET_ID]: "Пожалуйста, выберите напоминание, которое вы хотите удалить.",

        action_messages[Actions.ADD_TIMEZONE]: "Этот функционал связан с местным временем. Чтобы позволить вам пользоваться им, мне \
необходимо знать ваш часовой пояс. К сожалению, я не могу определить его без вашей помощи. Пожалуйста, нажмите на кнопку ниже, чтобы \
отправить мне свою локацию. Я НЕ буду хранить ее, и использую ее только сейчас для определения вашего часового пояса. Если у вас \
есть какие-либо сомнения по поводу того, что я делаю с вашей локацией, вы можете ознакомиться с моим исходным кодом на \
https://github.com/stonekite/eshkoleso_bot (./handlers/misc.py, метод add_timezone).",
        action_messages[Actions.ADD_TIMEZONE_SET_TIMEZONE]: "🌍 Отправить координаты",

        action_messages[Actions.DONE]: "Готово! ✔️",
        action_messages[Actions.ERROR]: "Извините, что-то пошло не так.",
        action_messages[Actions.USER_ERROR]: "Извините, я не понял."
    })
})

translation_items = []
for translation in translations.values():
    translation_items += translation.items()
translation_keys = set(item[0] for item in translation_items)


def t(text: Union[str, Actions], user_id: int) -> str:
    language = get_language(user_id)
    if type(text) == Actions:
        text = action_messages.get(text)
    return text if language == "en" else translations.get(language, {}).get(text, text)


def t_get_all_options(text: str) -> list[str]:
    return list(set(text, ([translation for translation in language.get(text, text)] for language in translations.values())))


def is_in_translation_keys(text: str):
    return text in translation_keys


def matching_key(text: str):
    for item in translation_items:
        if item[1] == text:
            return item[0]
    
    return text
