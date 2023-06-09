import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass


from src.constants import SnakeDirection

if typing.TYPE_CHECKING:
    from src.game_engine.game_logic.matrix import Matrix2D


@dataclass
class SnakeBody:
    """Part of the snake.
    It represents board's field.
    x - width, y - height."""

    x: int
    y: int


class SnakeAbs(ABC):
    def __init__(self, start_x: int, start_y: int, direction=SnakeDirection.UP):
        self.direction = direction
        self._body: typing.List[SnakeBody] = [SnakeBody(x=start_x, y=start_y)]

    def head(self):
        head_i = 0

        if len(self._body) == head_i:
            raise IndexError(head_i, self._body)

        return self._body[head_i]

    def tail(self):
        tail_i = len(self._body) - 1

        if tail_i < 0:
            raise IndexError(tail_i, self._body)

        return self._body[tail_i]

    def die(self):
        """ Kill a snake. """
        raise NotImplementedError(self)

    @abstractmethod
    def move(self, matrix: "Matrix2D"):
        """Change each snake's body part coordinates based on current direction."""


class NormalSnake(SnakeAbs):
    def move(self, matrix: "Matrix2D"):
        pass
