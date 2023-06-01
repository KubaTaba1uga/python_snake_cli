from copy import deepcopy

from src.constants import GAME_MENU_CTX

_MENU_FIELDS_MAP_TEMPLATE = {
    GAME_MENU_CTX.MENU: {
        "title": "Game Menu",
        "fields": {
            "create_new_session": {
                "display_name": "Start New Game",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CREATE_NEW_SESSION,
                "disabled": False,
            },
            # "save_current_session": {
            #     "display_name": "Start New Game",
            #     "selected": False,
            #     "next_ctx": GAME_MENU_CTX.SAVE_CURRENT_SESSION,
            #     "disabled": False,
            # },
        },
    },
    GAME_MENU_CTX.CREATE_NEW_SESSION: {
        "title": "Board Choice",
        "fields": {
            # this part should be generated dynamically based on BoardABS children.
            # below is only ex.
            "0": {
                "display_name": "No walls",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CHOOSE_DIFFICULTY,
                "disabled": False,
            },
        },
    },
    GAME_MENU_CTX.CHOOSE_DIFFICULTY: {
        "title": "Difficulty Choice",
        "fields": {
            # this part should be generated dynamically based on DifficultyABS children.
            # below is only ex.
            "1": {
                "display_name": "Easy",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.MENU,
                # "next_ctx": GAME_MENU_CTX.PLAY,
                "disabled": False,
            },
        },
    },
}


def _unselect_all_fields_before_execution(function):
    """ only one field can be selected in the ctx """

    def wrapped_function(self, *args, **kwargs):
        for field in self._get_fields():
            self._unselect_field(field)

        return function(self, *args, **kwargs)

    return wrapped_function


class GameMenu:
    DEFAULT_GAME_MENU_CTX = GAME_MENU_CTX.MENU

    def __init__(self):
        self.ctx = self.DEFAULT_GAME_MENU_CTX
        self.fields_map = deepcopy(_MENU_FIELDS_MAP_TEMPLATE)
        self.current_session = None

    @_unselect_all_fields_before_execution
    def select_field(self, field_id: str):
        self._get_field(field_id)["selected"] = True

    def _unselect_field(self, field_id: str):
        self._get_field(field_id)["selected"] = False

    def _disable_field(self, field_id: str):
        self._get_field(field_id)["disabled"] = True

    def _get_field(self, field_id: str) -> dict:
        return self.fields_map[self.ctx]["fields"][field_id]

    def _get_fields(self) -> dict:
        return self.fields_map[self.ctx]["fields"]

    def process_selected_field(self):
        for field in self._get_fields().values():
            if field["selected"]:
                self.ctx = field["next_ctx"]
                return
