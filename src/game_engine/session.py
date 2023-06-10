import typing
from dataclasses import dataclass

if typing.TYPE_CHECKING:
    from src.game_engine.difficulty import DifficultyAbs
    from src.game_engine.game_logic.board import BoardAbs


@dataclass
class Session:
    difficulty: "DifficultyAbs"
    board_class: typing.Type["BoardAbs"]
    # board: typing.Optional["BoardAbs"]
