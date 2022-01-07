from utils.helpers.menu import update_menu
from utils.helpers.misc import get_user_id
from utils.actions import Actions
from utils.l10n import t


def handle_closing_action(update, context, action):
    update_menu(update, context, action)
