import typing
from copy import deepcopy

from src.constants import GAME_MENU_CTX

_MENU_FIELDS_MAP_TEMPLATE = {
    GAME_MENU_CTX.MENU: {
        "title": "Game Menu",
        "fields": {
            0: {
                "display_name": "Start New Game",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.CHOOSE_BOARD,
                "disabled": False,
            },
            1: {
                "display_name": "Save Current Game",
                "selected": False,
                "next_ctx": GAME_MENU_CTX.SAVE_CURRENT_SESSION,
                "disabled": False,
            },
        },
    },
    GAME_MENU_CTX.CHOOSE_BOARD: {
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
                "next_ctx": GAME_MENU_CTX.PLAY_NEW,
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
    """ Manages GameSession for GameEngine."""

    DEFAULT_GAME_MENU_CTX = GAME_MENU_CTX.MENU

    def __init__(self, session=None):
        self.ctx = self.DEFAULT_GAME_MENU_CTX
        self.fields_map = deepcopy(_MENU_FIELDS_MAP_TEMPLATE)
        self.session = session

    def select_next_field(self):
        # Mapped to: arrow up
        field_id, _ = self._get_selected_field()
        self.select_field(field_id + 1)

    def select_previous_field(self):
        # Mapped to: arrow down
        field_id, _ = self._get_selected_field()
        self.select_field(field_id - 1)

    @_overload_field_id
    @_unselect_all_fields_before_execution
    def select_field(self, field_id: str):
        self._get_field(field_id)["selected"] = True

    def set_new_ctx(self):
        # Mapped to: Enter
        _, field = self._get_selected_field()
        self.ctx = field["next_ctx"]

    def is_session_ready(self):
        return self.ctx in [GAME_MENU_CTX.PLAY_NEW, GAME_MENU_CTX.PLAY_LOADED]

    def process_ctx(self):
        GAME_MENU_CTX_PROCESS_FUNC_MAP = {
            GAME_MENU_CTX.PLAY_NEW: self._save_session,
        }

        GAME_MENU_CTX_PROCESS_FUNC_MAP[self.ctx]()

    def _save_session(self):
        """create session based on selected:
        1. board
        2. difficulty
        """

        board_ctx, difficulty_ctx, current_ctx = (
            GAME_MENU_CTX.CHOOSE_BOARD,
            GAME_MENU_CTX.CHOOSE_DIFFICULTY,
            self.ctx,
        )

        try:
            self.ctx = board_ctx
            board_field_id, _ = self._get_selected_field()

            self.ctx = difficulty_ctx
            difficulty_field_id, _ = self._get_selected_field()
        finally:
            self.ctx = current_ctx

        # board_class = get_board_class_by_id(board_field_id)
        difficulty_class = get_difficulty_class_by_id(difficulty_field_id)

    def _get_selected_field(self) -> tuple:
        for field_id, field in self._get_fields().items():
            if field["selected"]:
                return field_id, field

        raise NotImplementedError(self.fields_map, self.ctx)

    def _unselect_field(self, field_id: str):
        self._get_field(field_id)["selected"] = False

    def _disable_field(self, field_id: str):
        self._get_field(field_id)["disabled"] = True

    def _get_field(self, field_id: str) -> dict:
        return self.fields_map[self.ctx]["fields"][field_id]

    def _get_fields(self) -> dict:
        return self.fields_map[self.ctx]["fields"]
