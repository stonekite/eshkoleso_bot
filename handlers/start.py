from telegram import Update
from telegram.ext import CallbackContext
from utils.data.user_data import ensure_user_exists
from utils.helpers.menu import update_menu
from utils.l10n import t

def start_handler(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    ensure_user_exists(user_id, update.effective_chat.id)
    update_menu(update, context, message=t("Welcome!", user_id))
