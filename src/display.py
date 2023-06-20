import shutil
import sys
import typing
from abc import abstractmethod
from threading import Event
from threading import Thread
from time import sleep

from src.constants import BOARD_FIELD_TYPE
from src.constants import DEFAULT_GAME_FREQUENCY_IN_HZ
from src.constants import GAME_ENGINE_CTX
from src.game_engine.utils.si_utils import get_seconds_from_hz
from src.logging import log_display_error
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
    # less than 300hz makes LARGE board lagging on HARD
    DEFAULT_FREQ_IN_HZ = DEFAULT_GAME_FREQUENCY_IN_HZ * 3

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
        self._thread: Thread = Thread(target=self._process)
        self._stop_thread: Event = Event()

        self.CTX_RENDER_MAP = self._init_ctx_render_map()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        self.stop()

    def _init_ctx_render_map(self) -> dict:
        return {
            GAME_ENGINE_CTX.GAME: self._render_game_engine,
            GAME_ENGINE_CTX.PAUSE: self._render_game_engine,
            GAME_ENGINE_CTX.MENU: self._render_game_menu,
        }

    def _render(self):
        self.render(self.CTX_RENDER_MAP, self._game_engine.ctx)

    def _render_game_menu(self):
        self.render_game_menu(self._game_engine, self.width(), self.height())

    def _render_game_engine(self):
        self.render_game_engine(self._game_engine, self.width(), self.height())

    @log_display_error
    def _process(self):
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


class BashDisplay(DisplayAbs):
    _BOARD_FIELD_STRING_MAP = {
        BOARD_FIELD_TYPE.GROUND: lambda: paint_white(" ", True),
        BOARD_FIELD_TYPE.SNAKE: lambda: paint_blue(" ", True),
        BOARD_FIELD_TYPE.WALL: lambda: paint_black(" ", True),
        BOARD_FIELD_TYPE.FRUIT: lambda: paint_red(" ", True),
    }

    @classmethod
    @_print_result
    def render_game_engine(
        cls, game_engine: "GameEngine", width: int, height: int
    ) -> str:
        """Display gameplay."""

        max_x_i, max_y_i = cls._get_max_render_size(game_engine, width, height)

        lines_to_print: typing.List[str] = []

        for y_i in range(max_y_i):
            line = cls._format_game_engine_row(game_engine, max_x_i, y_i)
            lines_to_print.append(line)

        cls._fill_empty_space(
            lines_to_print, height - 1  # do not delete `- 1` (hack but working),
        )

        return cls.format_lines(lines_to_print, None)

    @classmethod
    def _get_max_render_size(cls, game_engine: "GameEngine", width: int, height: int):
        """Check how much columns and rows of current gameplay
        can be rendered on the display."""
        max_x_i, max_y_i = game_engine.board.size

        # Count height and width in advance
        # So trimming is redundant
        if width < max_x_i:
            max_x_i = width
        if height < max_y_i:
            max_y_i = height

        return max_x_i, max_y_i

    @classmethod
    def _format_game_engine_row(
        cls, game_engine: "GameEngine", width: int, height: int
    ):
        line_l: typing.List[str] = []

        for i in range(width):
            board_field = game_engine.board.matrix.get(i, height)
            line_l.append(cls._render_board_field(board_field))

        return "".join(line_l)

    @classmethod
    def _render_board_field(cls, board_field: BOARD_FIELD_TYPE) -> str:
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

        cls._fill_empty_space(lines_to_print, height - 1)

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
        FIELD_LINE_SYNTAX, DISABLED_FIELD_SYNTAX = (
            "      - {field_name}",
            "        {field_name}",
        )

        field_name = field["display_name"]

        if field["selected"]:
            field_name = cls.render_selected(field_name)

        line = FIELD_LINE_SYNTAX.format(field_name=field_name)

        if field["disabled"]:
            line = DISABLED_FIELD_SYNTAX.format(field_name=field_name)

        return cls.format_line(line, width)

    @classmethod
    def format_line(cls, line: str, width: int) -> str:
        line = line[:width]
        return move_cursor_to_line_beginning(line)

    @classmethod
    def render_selected(cls, line: str) -> str:
        return paint_red(line, True)

    @classmethod
    def format_lines(
        cls, lines: typing.List[str], height: typing.Optional[int] = None
    ) -> str:
        lines = lines[:height]
        return "\n".join(lines)

    @classmethod
    def print(cls, lines: str):
        sys.stdout.write(lines)
        sys.stdout.flush()

    @classmethod
    def width(cls):
        # this makes display to not fold the line but cut it
        return shutil.get_terminal_size()[0]

    @classmethod
    def height(cls):
        # this makes display to not crash animation when terminal resized
        return shutil.get_terminal_size()[1]

    @classmethod
    def _fill_empty_space(cls, lines_to_print, height):
        rendered_lines_height = len(lines_to_print) - 1
        lines_to_fill = height - rendered_lines_height

        for _ in range(lines_to_fill):
            # Add empty strings to represent empty space
            lines_to_print.append("")
