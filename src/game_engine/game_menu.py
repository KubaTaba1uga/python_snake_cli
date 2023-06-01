from copy import deepcopy

from src.constants import GAME_MENU_CTX

_MENU_FIELDS_MAP_TEMPLATE = {
    GAME_MENU_CTX.MENU: {
        "title": "Game Menu",
        "fields": {
            0: {
                "display_name": "Start New Game",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CREATE_NEW_SESSION,
                "disabled": False,
            },
            1: {
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
            # below is only ex.
            0: {
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
            0: {
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


def _overload_field_id(function):
    """If field_id drops below 0 assign the biggest id to it.
    If field_id raises over the biggest id assign 0 to it."""

    def wrapped_function(self, field_id, *args, **kwargs):
        fields = self._get_fields()

        max_id, min_id = len(fields) - 1, 0

        if field_id > max_id:
            field_id = min_id
        elif field_id < min_id:
            field_id = max_id

        return function(self, field_id, *args, **kwargs)

    return wrapped_function


class GameMenu:
    DEFAULT_GAME_MENU_CTX = GAME_MENU_CTX.MENU

    def __init__(self):
        self.ctx = self.DEFAULT_GAME_MENU_CTX
        self.fields_map = deepcopy(_MENU_FIELDS_MAP_TEMPLATE)
        self.current_session = None

    def select_next_field(self):
        for field_id, field in self._get_fields().items():
            if field["selected"]:
                self.select_field(field_id + 1)
                return

        raise NotImplementedError(self)

    def select_previous_field(self):
        for field_id, field in self._get_fields().items():
            if field["selected"]:
                self.select_field(field_id - 1)
                return

        raise NotImplementedError(self)

    @_overload_field_id
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
