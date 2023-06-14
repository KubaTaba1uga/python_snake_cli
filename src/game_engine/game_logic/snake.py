import typing
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

from src.logging import log_snake_info
from src.constants import BoardFieldType
from src.constants import SnakeDirection
from src.errors import SnakeDied
from src.errors import ValidationError

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
        self._direction = direction
        self._body: typing.List[SnakeBody] = [SnakeBody(x=start_x, y=start_y)]

    def __getitem__(self, i):
        return self._body[i]

    def __len__(self):
        return len(self._body)

    def head(self):
        return self._body[0]

    def tail(self):
        return self._body[-1]

    def die(self):
        """Kill a snake."""
        raise SnakeDied(self)

    def set_direction(self, direction: SnakeDirection):
        try:
            self.validate_direction(direction)
        except ValidationError:
            return

        self._direction = direction

    @abstractmethod
    def move(self, matrix: "Matrix2D"):
        """Moves snake body and show the move on matrix."""
        pass

    @abstractmethod
    def validate_direction(self, new_direction: SnakeDirection):
        pass


def _log_snake_head(function):
    LOG_SYNTAX = "Snake moved from x={old_x}, y={old_y} to x={new_x}, y={new_y}"

    def wrapped_func(self, *args, **kwargs):
        head_before = self.head()

        try:
            result = function(self, *args, **kwargs)
        except Exception as err:
            log_snake_info("ERROR")
            exit(1)

        head_after = self.head()

        log_snake_info(
            LOG_SYNTAX.format(
                old_x=head_before.x,
                new_x=head_after.x,
                old_y=head_before.y,
                new_y=head_after.y,
            )
        )

        return result

    return wrapped_func


class NormalSnake(SnakeAbs):
    @_log_snake_head
    def move(self, matrix: "Matrix2D"):
        self._clear_tail(matrix)

        self._move(matrix)

        self._render_head(matrix)

        # this is required in case fruit was eaten
        self._render_tail(matrix)

    def _clear_tail(self, matrix: "Matrix2D"):
        tail = self.tail()
        matrix.set(BoardFieldType.GROUND, tail.x, tail.y)

    def _render_tail(self, matrix: "Matrix2D"):
        tail = self.tail()
        matrix.set(BoardFieldType.SNAKE, tail.x, tail.y)

    def _render_head(self, matrix: "Matrix2D"):
        tail = self.head()
        matrix.set(BoardFieldType.SNAKE, tail.x, tail.y)

    def _move(self, matrix: "Matrix2D"):
        """Move snake by creating new head and deleting a tail."""
        new_head_x, new_head_y = self._calculate_new_head_coordinates(matrix)

        self._grow_head(new_head_x, new_head_y)

        self._process_move(matrix, new_head_x, new_head_y)

        self._shrink()

    def _process_move(self, matrix: "Matrix2D", move_x: int, move_y: int):
        FIELD_TYPE_FUNC_MAP = {
            BoardFieldType.WALL: self.die,
            BoardFieldType.SNAKE: self.die,
            BoardFieldType.FRUIT: self._grow_dummy_tail,
        }

        field_type = matrix.get(move_x, move_y)

        try:
            FIELD_TYPE_FUNC_MAP[field_type]()
        except KeyError:
            pass

    def _calculate_new_head_coordinates(
        self, matrix: "Matrix2D"
    ) -> typing.Tuple[int, int]:
        current_head = self.head()
        current_head_x, current_head_y = current_head.x, current_head.y

        new_head_x, new_head_y = self._calculate_new_head_x(
            matrix, current_head_x, self._direction
        ), self._calculate_new_head_y(matrix, current_head_y, self._direction)

        return new_head_x, new_head_y

    @classmethod
    def _calculate_new_head_x(
        cls, matrix: "Matrix2D", current_head_x: int, direction: SnakeDirection
    ) -> int:
        DIRECTION_MOVE_MAP = {
            SnakeDirection.LEFT: cls._move_prev,
            SnakeDirection.RIGHT: cls._move_next,
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
            SnakeDirection.UP: cls._move_prev,
            SnakeDirection.DOWN: cls._move_next,
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

        return new if new <= max_i else min_i

    @classmethod
    def _move_prev(cls, current: int, max_i: int, min_i: int) -> int:
        new = current - 1

        return new if new >= min_i else max_i

    def _grow_head(self, x, y):
        new_head = SnakeBody(x, y)

        self._body.insert(0, new_head)

    def _grow_dummy_tail(self):
        dummy_tail = SnakeBody(-1, -1)

        self._body.append(dummy_tail)

    def _shrink(self):
        self._body.pop()

    def validate_direction(self, new_direction: SnakeDirection):
        SELF_DIRECTION_FORBIDDEN_DIRECTION_MAP = {
            SnakeDirection.UP: SnakeDirection.DOWN,
            SnakeDirection.DOWN: SnakeDirection.UP,
            SnakeDirection.LEFT: SnakeDirection.RIGHT,
            SnakeDirection.RIGHT: SnakeDirection.LEFT,
        }

        if new_direction == SELF_DIRECTION_FORBIDDEN_DIRECTION_MAP[self._direction]:
            raise ValidationError(
                new_direction, self._direction, SELF_DIRECTION_FORBIDDEN_DIRECTION_MAP
            )


# TO-DO
# creates lazy snake - bigger it gets slower it moves
# create fit snake - bigger he gets quicker he moves
