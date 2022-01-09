from telegram.ext import CallbackContext
from telegram.update import Update
from time import time
from requests import get
from utils.data.user_data import set_timezone
from utils.keys import timezone_token
from utils.actions import Actions
from utils.helpers.menu import update_menu
from utils.helpers.misc import get_user_id


def add_timezone(update: Update, context: CallbackContext):
    user_id = get_user_id(update)
    location = update.message.location

    response = get(f"https://maps.googleapis.com/maps/api/timezone/json\
?location={location.latitude}%2C{location.longitude}&timestamp={time()}&key={timezone_token}").json()
    set_timezone(user_id, response.get("rawOffset") / 60 / 60)

    handle_closing_action(update, context, Actions.DONE)


def handle_closing_action(update: Update, context: CallbackContext, action: Actions):
    update_menu(update, context, action)
