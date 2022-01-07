from enum import IntEnum, auto


class Actions(IntEnum):
    SHOW_MEDS = auto()
    ADD_MEDS = auto()
    ADD_MEDS_SET_NAME = auto()
    REMOVE_MEDS = auto()
    REMOVE_MEDS_SET_INDEX = auto()

    SHOW_JOURNAL_QUESTIONS = auto()
    ADD_JOURNAL_QUESTION = auto()
    REMOVE_JOURNAL_QUESTION = auto()
    ADD_JOURNAL_RESPONSE = auto()

    SHOW_REMINDERS = auto()
    ADD_REMINDER = auto()
    REMOVE_REMINDER = auto()
    ADD_REMINDER_RESPONSE = auto()

    SHOW_INTERVAL_REMINDERS = auto()
    ADD_INTERVAL_REMINDER = auto()
    REMOVE_INTERVAL_REMINDER = auto()
    ADD_INTERVAL_REMINDER_RESPONSE = auto()
    START_INTERVAL_REMINDERS = auto()

    DONE = auto()
    ERROR = auto()
    USER_ERROR = auto()


action_messages = dict({
    Actions.SHOW_MEDS: "My meds",
    Actions.ADD_MEDS: "Add meds",
    Actions.ADD_MEDS_SET_NAME: "Please enter the name of the meds.",
    Actions.REMOVE_MEDS: "Remove meds",
    Actions.REMOVE_MEDS_SET_INDEX: "Please select the meds you want to remove.",

    Actions.SHOW_JOURNAL_QUESTIONS: "My journal",
    Actions.ADD_JOURNAL_QUESTION: "Add question",
    Actions.REMOVE_JOURNAL_QUESTION: "Remove question",
    Actions.ADD_JOURNAL_RESPONSE: "Add answer",

    Actions.SHOW_REMINDERS: "My timed reminders",
    Actions.ADD_REMINDER: "Add reminder",
    Actions.REMOVE_REMINDER: "Remove reminder",
    Actions.ADD_REMINDER_RESPONSE: "Add answer",
    
    Actions.SHOW_INTERVAL_REMINDERS: "My interval reminders",
    Actions.ADD_INTERVAL_REMINDER: "Add reminder",
    Actions.REMOVE_INTERVAL_REMINDER: "Remove reminder",
    Actions.ADD_INTERVAL_REMINDER_RESPONSE: "Add answer",
    Actions.START_INTERVAL_REMINDERS: "Start interval reminders",

    Actions.DONE: "Done!",
    Actions.ERROR: "Sorry, something went wrong.",
    Actions.USER_ERROR: "Sorry, I didn't get that."
})
