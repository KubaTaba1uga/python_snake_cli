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
        """Kill a snake."""
        raise NotImplementedError(self)

    @abstractmethod
    def move(self, matrix: "Matrix2D"):
        """Change each snake's body part coordinates based on current direction."""


class NormalSnake(SnakeAbs):
    def move(self, matrix: "Matrix2D"):
        new_head_x, new_head_y = self._calculate_new_head_coordinates(matrix)
        self._grow(new_head_x, new_head_y)
        self._shrink()

    def _calculate_new_head_coordinates(self, matrix: "Matrix2D") -> typing.Tuple[int]:
        current_head = self.head()
        current_head_x, current_head_y = current_head.x, current_head.y

        new_head_x, new_head_y = self._calculate_new_head_x(
            matrix, current_head_x, self.direction
        ), self._calculate_new_head_y(matrix, current_head_y, self.direction)

        print(new_head_y)

        return new_head_x, new_head_y

    @classmethod
    def _calculate_new_head_x(
        cls, matrix: "Matrix2D", current_head_x: int, direction: SnakeDirection
    ) -> int:
        DIRECTION_MOVE_MAP = {
            SnakeDirection.LEFT: cls._move_next,
            SnakeDirection.RIGHT: cls._move_prev,
        }

        matrix_max_x_i, matrix_min_x_i = matrix.width() - 1, 0

        try:
            return DIRECTION_MOVE_MAP[direction](
                current_head_x, matrix_max_x_i, matrix_min_x_i
            )
        except KeyError:
            return current_head_x

    @classmethod
    def _calculate_new_head_y(
        cls, matrix: "Matrix2D", current_head_y: int, direction: SnakeDirection
    ) -> int:
        DIRECTION_MOVE_MAP = {
            SnakeDirection.UP: cls._move_next,
            SnakeDirection.DOWN: cls._move_prev,
        }

        matrix_max_y_i, matrix_min_y_i = matrix.height() - 1, 0

        try:
            return DIRECTION_MOVE_MAP[direction](
                current_head_y, matrix_max_y_i, matrix_min_y_i
            )
        except KeyError:
            return current_head_y

    @classmethod
    def _move_next(cls, current: int, max_i: int, min_i: int) -> int:
        new = current + 1

        return new if new < max_i else min_i

    @classmethod
    def _move_prev(cls, current: int, max_i: int, min_i: int) -> int:
        new = current - 1

        return new if new > min_i else max_i

    def _grow(self, x, y):
        new_head = SnakeBody(x, y)

        self._body.insert(0, new_head)

    def _shrink(self):
        self._body.pop()
