from src.constants import GAME_MENU_CTX

_MENU_FIELDS_STATUS_MAP = {
    "create_new_session": {
        "display_name": "Start New Game",
        "selected": False,
        "bounded_ctx": GAME_MENU_CTX.CREATE_NEW_SESSION,
        "disabled": False,
    },
    "save_current_session": {
        "display_name": "Start New Game",
        "selected": False,
        "bounded_ctx": GAME_MENU_CTX.CREATE_NEW_SESSION,
        "disabled": False,
    },
}


class GameMenu:
    DEFAULT_GAME_MENU_CTX = GAME_MENU_CTX.MENU

    def __init__(self):
        self.ctx = self.DEFAULT_GAME_MENU_CTX
