import typing


if typing.TYPE_CHECKING:
    from src.game_engine.difficulty import DifficultyAbs
    from src.game_engine.game_logic.board import BoardAbs
    from src.game_engine.game_logic.size import SizeAbs


class Session:
    def __init__(
        self,
        difficulty: "DifficultyAbs",
        board_class: typing.Type["BoardAbs"],
        size_class: typing.Type["SizeAbs"],
    ):
        pass

    board: typing.Optional["BoardAbs"]
