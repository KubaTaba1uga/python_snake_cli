import typing
from abc import abstractclassmethod
from time import sleep
from threading import Thread, Event

from src.constants import GAME_ENGINE_CTX
from src.game_engine.utils.si_utils import get_seconds_from_hz
from src.utils.abc_utils import ContextManagerAbs
from src.utils.ansi_utils import paint_red, paint_bold

if typing.TYPE_CHECKING:
    from src.game_engine.game_menu import GameMenu
    from src.game_engine.game_engine import GameEngine


class DisplayAbs(ContextManagerAbs):
    DEFAULT_FREQ_IN_HZ = 1

    @classmethod
    def sleep(cls):
        sleep(get_seconds_from_hz(cls.DEFAULT_FREQ_IN_HZ))

    def __init__(self, game_engine: "GameEngine", width: int, height: int):
        self._game_engine: "GameEngine" = game_engine
        self._width: int = width
        self._height: int = height
        self._thread: Thread = Thread(target=self._start)
        self._stop_thread: Event = Event()

    @abstractclassmethod
    def render_game_menu(
        cls, game_engine: "GameEngine", width: int, height: int
    ) -> str:
        """ Display game's menu. GameEngine """
        pass

    # @abstractclassmethod
    def render_game_engine(cls, game_engine: "GameEngine"):
        """ Display gameplay. """
        pass

    @classmethod
    def _render(cls, game_engine: "GameEngine"):
        CTX_RENDER_MAP = {
            GAME_ENGINE_CTX.GAME: cls.render_game_engine,
            GAME_ENGINE_CTX.MENU: cls.render_game_menu,
        }

        CTX_RENDER_MAP[game_engine.ctx](game_engine)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_value, exc_tryceback):
        self.stop()

    def render(self):
        self._render(self._game_engine)

    def _start(self):
        while True:
            self.render()
            self.sleep()

            if self._stop_thread.is_set():
                break

    def start(self):
        self._thread.start()

    def stop(self):
        self._stop_thread.set()


class BashDisplay(DisplayAbs):
    @classmethod
    def render_game_menu(
        cls, game_engine: "GameEngine", width: int, height: int
    ) -> str:
        """ Display game's menu. Returns string of what was displayed. """
        game_menu_fields, game_menu = (
            game_engine.game_menu.get_fields(),
            game_engine.game_menu,
        )

        title_line = cls.format_title(game_menu.get_title())

        lines_to_print = [title_line]

        for field in game_menu_fields.values():
            lines_to_print.append(cls.format_field(field))

        for _ in range(height - len(lines_to_print) - 1):
            # Add empty strings to fill space
            lines_to_print.append("")

        rendered_lines = cls.format_lines(lines_to_print)

        cls.print(rendered_lines)

        return rendered_lines

    @classmethod
    def validate_height(cls, height: int, fields_len: int):
        if height < fields_len + 1:
            raise ValueError(height, fields_len)

    @classmethod
    def validate_width(cls, width: int, fields: dict):

        max_field_length = 0
        for field in fields.values():
            if (field_length := len(cls.format_field(field))) > max_field_length:
                max_field_length = field_length

        if width < max_field_length:
            raise ValueError(width, max_field_length)

    @classmethod
    def format_title(cls, title: str) -> str:
        TITLE_LINE_SYNTAX = "   {title}"

        title = title.capitalize()
        title = paint_bold(title)

        return TITLE_LINE_SYNTAX.format(title=title)

    @classmethod
    def format_field(cls, field: dict) -> str:
        FIELD_LINE_SYNTAX = "      - {field_name}"

        field_name = field["display_name"]

        if field["selected"]:
            field_name = cls.render_selected(field_name)

        return FIELD_LINE_SYNTAX.format(field_name=field_name)

    @classmethod
    def render_selected(cls, line: str) -> str:
        return paint_red(line, True)

    @classmethod
    def format_lines(cls, lines: typing.List[str]) -> str:
        return "\n".join(lines)

    @classmethod
    def print(cls, lines: str):
        print(lines)
