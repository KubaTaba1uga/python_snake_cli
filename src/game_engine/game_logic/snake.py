import typing
from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass

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

    @abstractmethod
    def move(self, matrix: "Matrix2D"):
        """Moves snake body and show the move on matrix."""

        pass

    @abstractmethod
    def set_direction(self, direction: SnakeDirection):
        pass


class NormalSnake(SnakeAbs):
    def move(self, matrix: "Matrix2D"):
        self._clear_tail(matrix)

        self._move(matrix)

        self._render_head(matrix)
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

    def set_direction(self, direction: SnakeDirection):
        """Assign new direction to the snake.
        Validates direction's value, before performing assignment."""

        DIRECTION_VALIDATE_MAP = {
            SnakeDirection.UP: self._validate_up_direction,
            SnakeDirection.DOWN: self._validate_down_direction,
            SnakeDirection.LEFT: self._validate_left_direction,
            SnakeDirection.RIGHT: self._validate_right_direction,
        }

        try:
            DIRECTION_VALIDATE_MAP[direction]()
        except ValidationError:
            raise ValueError(direction)
        except KeyError:
            pass

        self._direction = direction

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

    def _validate_up_direction(self):
        # do not allow snake to eat its neck
        try:
            snake_neck = self[1]
        except IndexError:
            return

        is_neck_over_the_head = snake_neck.y == self.head().y - 1

        if is_neck_over_the_head:
            raise ValidationError()

    def _validate_down_direction(self):
        # do not allow snake to eat its neck
        try:
            snake_neck = self[1]
        except IndexError:
            return

        is_neck_below_the_head = snake_neck.y == self.head().y + 1

        if is_neck_below_the_head:
            raise ValidationError()

    def _validate_left_direction(self):
        # do not allow snake to eat its neck
        try:
            snake_neck = self[1]
        except IndexError:
            return

        is_neck_next_to_the_head = snake_neck.x == self.head().x - 1

        if is_neck_next_to_the_head:
            raise ValidationError()

    def _validate_right_direction(self):
        # do not allow snake to eat its neck
        try:
            snake_neck = self[1]
        except IndexError:
            return

        is_neck_next_to_the_head = snake_neck.x == self.head().x + 1

        if is_neck_next_to_the_head:
            raise ValidationError()


# TO-DO
# creates lazy snake - bigger it gets slower it moves
# create fit snake - bigger he gets quicker he moves
