import typing
from datetime import datetime
from copy import copy

from src.constants import DEFAULT_GAME_FREQUENCY_IN_HZ, FIELD_TEMPLATE, GAME_MENU_CTX
from src.game_engine.difficulty import DifficultyEasy
from src.game_engine.difficulty import DifficultyHard
from src.game_engine.difficulty import DifficultyMedium

if typing.TYPE_CHECKING:
    from src.game_engine.difficulty import DifficultyAbs
    from src.game_engine.game_logic.board import BoardAbs
    from src.game_engine.game_logic.size import SizeAbs


DIFFICULTY_SLEEP_FREQ_IN_HZ_MAP: typing.Dict[typing.Type["DifficultyAbs"], float] = {
    DifficultyEasy: DEFAULT_GAME_FREQUENCY_IN_HZ / 8,
    DifficultyMedium: DEFAULT_GAME_FREQUENCY_IN_HZ / 6,
    DifficultyHard: DEFAULT_GAME_FREQUENCY_IN_HZ / 4,
}


class Session:
    """Manage board for game engine."""

    @classmethod
    def _init_difficulty(
        cls, difficulty_class: typing.Type["DifficultyAbs"]
    ) -> "DifficultyAbs":
        return difficulty_class()

    @classmethod
    def _init_size(cls, size_class: typing.Type["SizeAbs"]) -> "SizeAbs":
        return size_class()

    @classmethod
    def _init_board(
        cls,
        board_class: typing.Type["BoardAbs"],
        size: "SizeAbs",
        difficulty: "DifficultyAbs",
    ) -> "BoardAbs":
        return board_class(
            width=size.width(),
            height=size.height(),
            sleep_freq=DIFFICULTY_SLEEP_FREQ_IN_HZ_MAP[difficulty.__class__],
        )

    def __init__(
        self,
        difficulty_class: typing.Type["DifficultyAbs"],
        board_class: typing.Type["BoardAbs"],
        size_class: typing.Type["SizeAbs"],
    ):
        self.start_time: datetime = datetime.now()
        self.end_time: typing.Optional[datetime] = None

        self._difficulty_class = difficulty_class
        self._board_class = board_class
        self._size_class = size_class

        self._difficulty = self._init_difficulty(self._difficulty_class)
        self._size = self._init_size(self._size_class)
        self._board = self._init_board(self._board_class, self._size, self._difficulty)

    def is_session_finished(self):
        return self.end_time is None

    def finish(self):
        if self.is_session_finished():
            raise ValueError(self.end_time)

        self.end_time = datetime.now()

    @property
    def board(self):
        return self._board


# Inheritance by session is done only to keep typing clean.
class SessionDummy(Session):
    """Dummy session doesn't have any capability.
    Allow objects creation. Do not allow objects usage."""

    # Don't use dummy session in user environment. Providing
    #  it allows to get rid of optional type so makes less
    #  corner cases to handle > simpler code > quicker code.

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        raise NotImplementedError(args, kwargs)

    @property
    def board(self):
        raise NotImplementedError(self)


def generate_session_fields(session: Session) -> dict:
    FIELD_SYNTAX, NEXT_CTX = "{}: {}", GAME_MENU_CTX.MENU

    attributes_to_show = [
        "start_time",
        "end_time",
        "_difficulty_class",
        "_size_class",
        "_board_class",
    ]

    fields = {}

    for i, attribute in enumerate(attributes_to_show):
        attr_value, field = getattr(session, attribute), copy(FIELD_TEMPLATE)

        field["display_name"] = FIELD_SYNTAX.format(str(attribute), str(attr_value))
        field["next_ctx"] = NEXT_CTX

        fields[i] = field
    if len(fields) == 0:
        raise NotImplementedError("At least one attribute is required to show.")

    fields[0]["selected"] = True

    return fields
