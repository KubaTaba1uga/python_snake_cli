import typing

if typing.TYPE_CHECKING:
    from src.game_engine.difficulty import DifficultyAbs
    from src.game_engine.game_logic.board import BoardAbs
    from src.game_engine.game_logic.size import SizeAbs


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
    ) -> "BoardAbs":
        return board_class(width=size.width(), height=size.height())

    def __init__(
        self,
        difficulty_class: typing.Type["DifficultyAbs"],
        board_class: typing.Type["BoardAbs"],
        size_class: typing.Type["SizeAbs"],
    ):
        self._difficulty_class = difficulty_class
        self._board_class = board_class
        self._size_class = size_class

        self._difficulty = self._init_difficulty(self._difficulty_class)
        self._size = self._init_size(self._size_class)
        self._board = self._init_board(self._board_class, self._size)

    @property
    def board(self):
        return self._board


class SessionDummy(Session):
    """Dummy session doesn't have any capability.
    Allow objects creation. Do not allow objects usage."""

    # Don't use dummy session in user environment. Providing
    #  it allows to get rid of optional type so makes less
    #  corner cases to handle > simpler code > quicker code.

    def __init__(
        self,
        difficulty_class: typing.Type["DifficultyAbs"],
        board_class: typing.Type["BoardAbs"],
        size_class: typing.Type["SizeAbs"],
    ):
        self._difficulty_class = difficulty_class
        self._board_class = board_class
        self._size_class = size_class
