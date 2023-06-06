import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from src.game_engine.board import BoardAbs
    from src.game_engine.difficulty import DifficultyAbs


@dataclass
class Session:
    difficulty: "DifficultyAbs"
    board_class: typing.Type["BoardAbs"]
    # board: typing.Optional["BoardAbs"]
