import shutil
import sys
import typing
from abc import abstractmethod
from threading import Event
from threading import Thread
from time import sleep

from src.constants import BoardFieldType
from src.constants import GAME_ENGINE_CTX
from src.game_engine.utils.si_utils import get_seconds_from_hz
from src.utils.abc_utils import ContextManagerAbs
from src.utils.abc_utils import NonBlockingAbs
from src.utils.ansi_utils import move_cursor_to_line_beginning
from src.utils.ansi_utils import paint_black
from src.utils.ansi_utils import paint_blue
from src.utils.ansi_utils import paint_bold
from src.utils.ansi_utils import paint_red
from src.utils.ansi_utils import paint_white

if typing.TYPE_CHECKING:
    from src.game_engine.game_engine import GameEngine


class DisplayAbs(ContextManagerAbs, NonBlockingAbs):
    DEFAULT_FREQ_IN_HZ = 500

    @classmethod
    @abstractmethod
    def width(self):
        pass

    @classmethod
    @abstractmethod
    def height(self):
        pass

    @classmethod
    @abstractmethod
    def render_game_menu(
        cls, game_engine: "GameEngine", width: int, height: int
    ) -> str:
        """Display game's menu."""
        pass

    @classmethod
    @abstractmethod
    def render_game_engine(cls, game_engine: "GameEngine", width: int, height: int):
        """Display gameplay."""
        pass

    @classmethod
    def render(
        cls,
        ctx_render_map: typing.Dict[GAME_ENGINE_CTX, typing.Callable],
        game_engine_ctx: GAME_ENGINE_CTX,
    ):
        ctx_render_map[game_engine_ctx]()

    @classmethod
    def sleep(cls):
        sleep(get_seconds_from_hz(cls.DEFAULT_FREQ_IN_HZ))

    def __init__(
        self,
        game_engine: "GameEngine",
    ):
        self._game_engine: "GameEngine" = game_engine
        self._thread: Thread = Thread(target=self._start)
        self._stop_thread: Event = Event()

        self.CTX_RENDER_MAP = self._init_ctx_render_map()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        self.stop()

    def _init_ctx_render_map(self) -> dict:
        return {
            GAME_ENGINE_CTX.GAME: self.render_game_engine,
            GAME_ENGINE_CTX.MENU: self._render_game_menu,
        }

    def _render(self):
        self.render(self.CTX_RENDER_MAP, self._game_engine.ctx)

    def _render_game_menu(self):
        self.render_game_menu(self._game_engine, self.width(), self.height())

    def _render_game_engine(self):
        self.render_game_engine(self._game_engine, self.width(), self.height())

    def _start(self):
        while True:
            self._render()
            self.sleep()

            if self._stop_thread.is_set():
                break

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_thread.set()


def _print_result(function):
    def wrapped_func(cls, *args, **kwargs):
        result = function(cls, *args, **kwargs)
        cls.print(result)
        return result

    return wrapped_func


# TO-DO:
#  make lines formatters as decorators
#    - trimm width
#    - trim hight
#    - paint red
#    - style bold


class BashDisplay(DisplayAbs):
    _BOARD_FIELD_STRING_MAP = {
        BoardFieldType.GROUND: lambda: paint_white(" ", True),
        BoardFieldType.SNAKE: lambda: paint_blue(" ", True),
        BoardFieldType.WALL: lambda: paint_black(" ", True),
        BoardFieldType.FRUIT: lambda: paint_red(" ", True),
    }

    @classmethod
    @_print_result
    def render_game_engine(
        cls, game_engine: "GameEngine", width: int, height: int
    ) -> str:
        """Display gameplay."""

        max_x_i, max_y_i = game_engine.board.size, game_engine.board.size

        # Count height and width in advance
        # So trimming is redundant
        if width < max_x_i:
            max_x_i = width
        if height < max_y_i:
            max_y_i = height

        lines_to_print: typing.List[str] = []

        for y in range(max_y_i):
            # format board rows
            line_l: typing.List[str] = []

            for x in range(max_x_i):
                board_field = game_engine.board.matrix.get(x, y)
                line_l.append(cls._render_board_field(board_field))

            line: str = "".join(line_l)
            line = cls.format_line(line, None)
            lines_to_print.append(line)

        # format board columns
        cls._fill_empty_space(lines_to_print, height)

        return cls.format_lines(lines_to_print, None)

    @classmethod
    def _render_board_field(cls, board_field: BoardFieldType) -> str:
        return cls._BOARD_FIELD_STRING_MAP[board_field]()

    @classmethod
    @_print_result
    def render_game_menu(
        cls, game_engine: "GameEngine", width: int, height: int
    ) -> str:
        """Display game's menu. Returns string of what was displayed."""

        game_menu_fields, game_menu = (
            game_engine.game_menu.get_fields(),
            game_engine.game_menu,
        )

        title_line = cls.format_title(game_menu.get_title(), width)

        lines_to_print = ["", title_line]

        for field in game_menu_fields.values():
            lines_to_print.append(cls.format_field(field, width))

        cls._fill_empty_space(lines_to_print, height)

        rendered_lines = cls.format_lines(lines_to_print, height)

        return rendered_lines

    @classmethod
    def format_title(cls, title: str, width: int) -> str:
        TITLE_LINE_SYNTAX = "   {title}"

        title = title.capitalize()
        title = paint_bold(title)

        return cls.format_line(TITLE_LINE_SYNTAX.format(title=title), width)

    @classmethod
    def format_field(cls, field: dict, width: int) -> str:
        FIELD_LINE_SYNTAX = "      - {field_name}"

        field_name = field["display_name"]

        if field["selected"]:
            field_name = cls.render_selected(field_name)

        return cls.format_line(FIELD_LINE_SYNTAX.format(field_name=field_name), width)

    @classmethod
    def format_line(cls, line: str, width: typing.Optional[int]) -> str:
        line = line[:width]
        return move_cursor_to_line_beginning(line)

    @classmethod
    def render_selected(cls, line: str) -> str:
        return paint_red(line, True)

    @classmethod
    def format_lines(cls, lines: typing.List[str], height: typing.Optional[int]) -> str:
        lines = lines[:height]
        return "\n".join(lines)

    @classmethod
    def print(cls, lines: str):
        sys.stdout.write(lines)
        sys.stdout.flush()

    @classmethod
    def width(cls):
        return shutil.get_terminal_size()[0]

    @classmethod
    def height(cls):
        return shutil.get_terminal_size()[1]

    @classmethod
    def _fill_empty_space(cls, lines_to_print, height):
        rendered_lines_height = len(lines_to_print) - 1
        for _ in range(height - rendered_lines_height):
            # Add empty strings to fill empty space
            lines_to_print.append("")
