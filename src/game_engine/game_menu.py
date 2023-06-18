import typing
from copy import deepcopy

from src.constants import GAME_MENU_CTX
from src.constants import get_key_value_by_display_name
from src.errors import NoSelectedField
from src.game_engine.difficulty import DifficultyEasy
from src.game_engine.difficulty import DifficultyFieldAbs
from src.game_engine.difficulty import generate_difficulty_fields
from src.game_engine.game_logic.board import BoardFieldAbs
from src.game_engine.game_logic.board import BoardNoWalls
from src.game_engine.game_logic.board import generate_board_fields
from src.game_engine.game_logic.size import generate_size_fields
from src.game_engine.game_logic.size import SizeFieldAbs
from src.game_engine.game_logic.size import SizeSmall
from src.game_engine.session import generate_session_fields
from src.game_engine.session import Session
from src.game_engine.session import SessionDummy
from src.logging import log_snake_error

BOARD_NEXT_CTX = GAME_MENU_CTX.CHOOSE_SIZE
DIFFICULTY_NEXT_CTX = GAME_MENU_CTX.PLAY_NEW
SIZE_NEXT_CTX = GAME_MENU_CTX.CHOOSE_DIFFICULTY

_MENU_FIELDS_MAP_TEMPLATE = {
    GAME_MENU_CTX.MENU: {
        "title": "Game Menu",
        "fields": {
            0: {
                "display_name": "Start New Game",
                "selected": True,
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
    GAME_MENU_CTX.PLAY_NEW: {
        "title": "Game is loading...",
        "fields": {},
    },
    GAME_MENU_CTX.CHOOSE_BOARD: {
        "title": "Board Choice",
        "fields": generate_board_fields(BOARD_NEXT_CTX),
    },
    GAME_MENU_CTX.CHOOSE_SIZE: {
        "title": "Board Size Choice",
        "fields": generate_size_fields(SIZE_NEXT_CTX),
    },
    GAME_MENU_CTX.CHOOSE_DIFFICULTY: {
        "title": "Difficulty Choice",
        "fields": generate_difficulty_fields(DIFFICULTY_NEXT_CTX),
    },
    GAME_MENU_CTX.PLAY_END: {
        "title": "Snake is dead! You lost!",
        "fields": {
            0: {
                "display_name": "Continue",
                "selected": True,
                "next_ctx": GAME_MENU_CTX.SHOW_SESSION,
                "disabled": False,
            }
        },
    },
    GAME_MENU_CTX.SHOW_SESSION: {"title": "Session info", "fields": {}},
}


def _unselect_all_fields_before_execution(function):
    """only one field can be selected in the ctx"""

    def wrapped_function(self, *args, **kwargs):
        for field in self.get_fields():
            self._unselect_field(field)

        return function(self, *args, **kwargs)

    return wrapped_function


def _overload_field_id(function):
    """If field_id drops below 0 assign the biggest id to it.
    If field_id raises over the biggest id assign 0 to it."""

    def find_fields_to_select(fields):
        ids_to_overload = []

        for id_, field in fields.items():
            if field["disabled"]:
                continue

            ids_to_overload.append(id_)

        return ids_to_overload

    def wrapped_function(self, field_id, *args, **kwargs):
        fields = self.get_fields()

        ids_to_overload = find_fields_to_select(fields)

        try:
            max_id, min_id = ids_to_overload[-1], ids_to_overload[0]
        except IndexError:
            return function(self, field_id, *args, **kwargs)

        if field_id > max_id:
            field_id = min_id
        elif field_id < min_id:
            field_id = max_id

        return function(self, field_id, *args, **kwargs)

    return wrapped_function


def _allow_no_fields(function):
    def wrapped_function(self, *args, **kwargs):
        try:
            return function(self, *args, **kwargs)
        except NoSelectedField:
            return

    return wrapped_function


class GameMenu:
    """Manages GameSession for GameEngine."""

    DEFAULT_GAME_MENU_CTX = GAME_MENU_CTX.MENU

    DEFAULT_SESSION = SessionDummy(
        difficulty_class=DifficultyEasy, board_class=BoardNoWalls, size_class=SizeSmall
    )

    def __init__(self, session: typing.Optional[Session] = None):
        self.ctx = self.DEFAULT_GAME_MENU_CTX
        self.fields_map: dict = deepcopy(_MENU_FIELDS_MAP_TEMPLATE)

        if session is None:
            session = self.DEFAULT_SESSION

        self.session: Session = session

        self.USER_INPUT_FUNC_MAP = self._init_user_input_func_map()

    def _init_user_input_func_map(self):
        return {
            get_key_value_by_display_name("ENTER key"): self.set_new_ctx,
            get_key_value_by_display_name("UP ARROW key"): self.select_previous_field,
            get_key_value_by_display_name("DOWN ARROW key"): self.select_next_field,
        }

    @_allow_no_fields
    def select_next_field(self):
        field_id, _ = self._get_selected_field()
        self._select_field(field_id + 1)

    @_allow_no_fields
    def select_previous_field(self):
        field_id, _ = self._get_selected_field()
        self._select_field(field_id - 1)

    @_allow_no_fields
    def set_new_ctx(self):
        _, field = self._get_selected_field()
        self.ctx = field["next_ctx"]

    def is_session_ready(self) -> bool:
        return self.ctx in [GAME_MENU_CTX.PLAY_NEW, GAME_MENU_CTX.PLAY_LOADED]

    def get_fields(self) -> dict:
        return self.fields_map[self.ctx]["fields"]

    def get_title(self) -> str:
        return self.fields_map[self.ctx]["title"]

    @log_snake_error
    def process_ctx(self):
        GAME_MENU_CTX_PROCESS_FUNC_MAP = {
            GAME_MENU_CTX.PLAY_NEW: self._create_session,
        }

        try:
            GAME_MENU_CTX_PROCESS_FUNC_MAP[self.ctx]()
        except KeyError:
            pass

    @log_snake_error
    def show_session(self):
        self.ctx = GAME_MENU_CTX.PLAY_END

        self.fields_map[GAME_MENU_CTX.SHOW_SESSION]["fields"] = generate_session_fields(
            self.session
        )

    def _create_session(self):
        """create session based on selected:
        1. board
        2. difficulty
        """

        board_ctx, size_ctx, difficulty_ctx, current_ctx = (
            GAME_MENU_CTX.CHOOSE_BOARD,
            GAME_MENU_CTX.CHOOSE_SIZE,
            GAME_MENU_CTX.CHOOSE_DIFFICULTY,
            self.ctx,
        )

        def _get_fields_by_ctx(ctx):
            try:
                self.ctx = ctx
                return self._get_selected_field()
            finally:
                self.ctx = current_ctx

        board_field_id, _ = _get_fields_by_ctx(board_ctx)

        difficulty_field_id, _ = _get_fields_by_ctx(difficulty_ctx)

        size_field_id, _ = _get_fields_by_ctx(size_ctx)

        board_class, difficulty_class, size_class = (
            BoardFieldAbs.get_children_class_by_id(board_field_id),
            DifficultyFieldAbs.get_children_class_by_id(difficulty_field_id),
            SizeFieldAbs.get_children_class_by_id(size_field_id),
        )

        self.session = Session(
            board_class=board_class,
            difficulty_class=difficulty_class,
            size_class=size_class,
        )

    @_overload_field_id
    @_unselect_all_fields_before_execution
    def _select_field(self, field_id: str):
        self._get_field(field_id)["selected"] = True

    def _get_selected_field(self, ctx=None) -> tuple:
        for field_id, field in self.get_fields().items():
            if field["selected"]:
                return field_id, field

        raise NoSelectedField(self.fields_map, self.ctx)

    def _unselect_field(self, field_id: str):
        self._get_field(field_id)["selected"] = False

    def _disable_field(self, field_id: str):
        self._get_field(field_id)["disabled"] = True

    def _get_field(self, field_id: str) -> dict:
        return self.fields_map[self.ctx]["fields"][field_id]
