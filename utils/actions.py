from enum import IntEnum, auto


class Actions(IntEnum):
    SHOW_MEDS = auto()
    ADD_MEDS = auto()
    ADD_MEDS_SET_NAME = auto()
    REMOVE_MEDS = auto()
    REMOVE_MEDS_SET_ID = auto()

    SHOW_JOURNAL_QUESTIONS = auto()
    ADD_JOURNAL_QUESTION = auto()
    ADD_JOURNAL_QUESTION_SET_TEXT = auto()
    REMOVE_JOURNAL_QUESTION = auto()
    REMOVE_JOURNAL_QUESTION_SET_ID = auto()
    ADD_JOURNAL_ANSWER = auto()
    ADD_JOURNAL_TIME = auto()

    SHOW_REMINDERS = auto()
    ADD_REMINDER = auto()
    ADD_REMINDER_SET_MEDS = auto()
    ADD_REMINDER_SET_DOSAGE = auto()
    ADD_REMINDER_SET_WITH_FOOD = auto()
    ADD_REMINDER_SET_TIME = auto()
    REMOVE_REMINDER = auto()
    REMOVE_REMINDER_SET_ID = auto()
    ADD_REMINDER_RESPONSE = auto()

    SHOW_INTERVAL_REMINDERS = auto()
    ADD_INTERVAL_REMINDER = auto()
    ADD_INTERVAL_REMINDER_SET_MEDS = auto()
    ADD_INTERVAL_REMINDER_SET_DOSAGE = auto()
    ADD_INTERVAL_REMINDER_SET_WITH_FOOD = auto()
    ADD_INTERVAL_REMINDER_SET_REPETITIONS = auto()
    ADD_INTERVAL_REMINDER_SET_INTERVAL = auto()
    REMOVE_INTERVAL_REMINDER = auto()
    REMOVE_INTERVAL_REMINDER_SET_ID = auto()
    ADD_INTERVAL_REMINDER_RESPONSE = auto()
    START_INTERVAL_REMINDERS = auto()

    ADD_TIMEZONE = auto()
    ADD_TIMEZONE_SET_TIMEZONE = auto()

    STOP_JOB = auto()

    DONE = auto()
    ERROR = auto()
    USER_ERROR = auto()


action_messages = dict({
    Actions.SHOW_MEDS: "💊 My meds",
    Actions.ADD_MEDS: "➕ Add meds",
    Actions.ADD_MEDS_SET_NAME: "Please enter the name of the meds.",
    Actions.REMOVE_MEDS: "❌ Remove meds",
    Actions.REMOVE_MEDS_SET_ID: "Please select the meds you want to remove.",

    Actions.SHOW_JOURNAL_QUESTIONS: "📖 My journal",
    Actions.ADD_JOURNAL_QUESTION: "➕ Add question",
    Actions.ADD_JOURNAL_QUESTION_SET_TEXT: "Please enter the text of the question. Assume answers to be digits from 1 to 5.",
    Actions.REMOVE_JOURNAL_QUESTION: "❌ Remove question",
    Actions.REMOVE_JOURNAL_QUESTION_SET_ID: "Please select the question you want to remove.",
    Actions.ADD_JOURNAL_ANSWER: "➕ Add answer",
    Actions.ADD_JOURNAL_TIME: "Please enter the time you want to journal in the format of hh:mm - e.g., 18:00.",

    Actions.SHOW_REMINDERS: "⏰ My timed reminders",
    Actions.ADD_REMINDER: "➕ Add reminder",
    Actions.ADD_REMINDER_SET_MEDS: "Please select the meds you want to be reminded about.",
    Actions.ADD_REMINDER_SET_DOSAGE: "Please enter the dosage for this timed reminder - e.g., number of pills.",
    Actions.ADD_REMINDER_SET_WITH_FOOD: "Please select whether you want to be reminded to eat 30 minutes before taking these meds.",
    Actions.ADD_REMINDER_SET_TIME: "Please enter the time for this reminder in the format of hh:mm - e.g., 18:00.",
    Actions.REMOVE_REMINDER: "❌ Remove reminder",
    Actions.REMOVE_REMINDER_SET_ID: "Please select the reminder you want to remove.",
    Actions.ADD_REMINDER_RESPONSE: "➕ Add answer",
    
    Actions.SHOW_INTERVAL_REMINDERS: "⏰ My interval reminders",
    Actions.ADD_INTERVAL_REMINDER: "➕ Add reminder",
    Actions.ADD_INTERVAL_REMINDER_SET_MEDS: "Please select the meds you want to be reminded about.",
    Actions.ADD_INTERVAL_REMINDER_SET_DOSAGE: "Please enter the dosage for this interval reminder - e.g., number of pills.",
    Actions.ADD_INTERVAL_REMINDER_SET_WITH_FOOD: "Please select whether you want to be reminded to eat 30 minutes before taking these meds.",
    Actions.ADD_INTERVAL_REMINDER_SET_REPETITIONS: "Please select the number of times you want to be reminded in a day.",
    Actions.ADD_INTERVAL_REMINDER_SET_INTERVAL: "Please select the amount of hours between each reminder.",
    Actions.REMOVE_INTERVAL_REMINDER: "❌ Remove reminder",
    Actions.REMOVE_INTERVAL_REMINDER_SET_ID: "Please select the reminder you want to remove.",
    Actions.ADD_INTERVAL_REMINDER_RESPONSE: "➕ Add answer",
    Actions.START_INTERVAL_REMINDERS: "⏲️ Start interval reminders",

    Actions.ADD_TIMEZONE: "This functionality involves local times. To allow you to use it, I need to know your timezone. Unfortunately, \
I can't determine it without your help. Please tap the button below to send me your location. I will NOT be storing it and will only use it \
this once to determine your timezone. If you have any concerns about what I do with your location, please check my source code at \
https://github.com/stonekite/eshkoleso_bot (./handlers/misc.py, add_timezone method)",
    Actions.ADD_TIMEZONE_SET_TIMEZONE: "🌍 Send location",

    Actions.DONE: "Done! ✔️",
    Actions.ERROR: "Sorry, something went wrong.",
    Actions.USER_ERROR: "Sorry, I didn't get that."
})
