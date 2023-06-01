from copy import deepcopy

from src.constants import GAME_MENU_CTX

_MENU_FIELDS_MAP = {
    GAME_MENU_CTX.MENU: {
        "title": "Game Menu",
        "fields": {
            "create_new_session": {
                "display_name": "Start New Game",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CREATE_NEW_SESSION,
                "disabled": False,
            },
            "save_current_session": {
                "display_name": "Start New Game",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.SAVE_CURRENT_SESSION,
                "disabled": False,
            },
        },
    },
    GAME_MENU_CTX.CREATE_NEW_SESSION: {
        "title": "Board Choice",
        "fields": {
            # this part should be generated dynamically based on BoardABS children.
            # this is only ex.
            "choose_board": {
                "display_name": "Board Choice",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CHOOSE_DIFFICULTY,
                "disabled": False,
            },
        },
    },
    GAME_MENU_CTX.CHOOSE_DIFFICULTY: {
        "title": "Difficulty Choice",
        "fields": {
            # this part should be generated based on DifficultyABS children.
            # this is only ex.
            "choose_difficulty": {
                "display_name": "Difficulty Choice",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CHOOSE_DIFFICULTY,
                "disabled": False,
            },
        },
    },
}


class GameMenu:
    DEFAULT_GAME_MENU_CTX = GAME_MENU_CTX.MENU

    def __init__(self):
        self.ctx = self.DEFAULT_GAME_MENU_CTX
