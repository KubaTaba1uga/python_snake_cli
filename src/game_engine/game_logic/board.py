import typing
from abc import ABC
from abc import abstractmethod
from copy import copy
from dataclasses import dataclass
from random import randint
from time import sleep

from src.constants import BOARD_FIELD_TYPE
from src.constants import DEFAULT_GAME_FREQUENCY_IN_HZ
from src.constants import FIELD_TEMPLATE
from src.constants import GAME_MENU_CTX
from src.game_engine.game_logic.matrix import Matrix2D
from src.game_engine.game_logic.snake import NormalSnake
from src.game_engine.game_logic.snake import SnakeAbs
from src.game_engine.utils.si_utils import get_seconds_from_hz


@dataclass
class Coordinates:
    x: int
    y: int


class BoardFieldAbs(ABC):
    # Id is required by Menu, to link field with board.
    id: typing.Optional[int] = None

    @classmethod
    @abstractmethod
    def display_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def add_ids_to_children_classes(cls):
        """Ids are required by Menu, to reognize which field is seleted."""
        for i, sub_class in enumerate(cls.__subclasses__()):
            sub_class.id = i

    @classmethod
    def get_children_class_by_id(cls, id_):
        for sub_class in cls.__subclasses__():
            if sub_class.id == id_:
                return sub_class

        raise NotImplementedError(cls, id_)


class BoardAbs(ABC):
    DEFAULT_BOARD_FREQ_IN_HZ = DEFAULT_GAME_FREQUENCY_IN_HZ

    @classmethod
    @abstractmethod
    def _initiate_board_basic(self, matrix):
        """Fill matrix body with field types (GROUND, WALL)."""
        raise NotImplementedError(self, matrix)

    @classmethod
    @abstractmethod
    def _initiate_snake(self, matrix) -> SnakeAbs:
        """Fill matrix body with snake type fields and create snake obj."""
        raise NotImplementedError(self, matrix)

    @classmethod
    @abstractmethod
    def _create_fruits(self, matrix) -> typing.List[Coordinates]:
        """Create list of coordinates which represent fruits locations."""
        raise NotImplementedError(self, matrix)

    @classmethod
    @abstractmethod
    def _render_fruits(self, matrix, fruits: typing.List[Coordinates]):
        """Reflects fruits on matrix.
        If fruit coordinates are taken by snake,
           deletes fruit from fruits list.
        """
        raise NotImplementedError(self, matrix, fruits)

    @classmethod
    def sleep(cls, time_in_sec: int):
        sleep(time_in_sec)

    def _sleep(self):
        seconds_to_sleep = get_seconds_from_hz(self._sleep_freq)
        sleep(seconds_to_sleep)

    def __init__(
        self, width: int, height: int, sleep_freq: typing.Optional[float] = None
    ):
        self.matrix = Matrix2D(width=width, height=height)

        self._initiate_board_basic(self.matrix)

        self.snake: SnakeAbs = self._initiate_snake(self.matrix)

        self.fruits: typing.List[Coordinates] = []

        if sleep_freq is None:
            sleep_freq = self.DEFAULT_BOARD_FREQ_IN_HZ

        self._sleep_freq = sleep_freq

    def process(self):
        if self.are_fruits_empty:
            self.fruits = self._create_fruits(self.matrix)

        self._render_fruits(self.matrix, self.fruits)

        self.move_snake()

        self._sleep()

    def move_snake(self):
        self.snake.move(self.matrix)

    @property
    def are_fruits_empty(self) -> bool:
        return len(self.fruits) == 0

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self.matrix.width(), self.matrix.height()


class BoardNoWalls(BoardAbs, BoardFieldAbs):
    @classmethod
    def display_name(cls) -> str:
        # This is required to generate menu's fields.
        return "No walls"

    @classmethod
    def _initiate_board_basic(self, matrix):
        """Fill matrix body with field types (GROUND, WALL)."""
        for x in range(matrix.width()):
            for y in range(matrix.height()):
                matrix.set(BOARD_FIELD_TYPE.GROUND, x, y)

    @classmethod
    def _initiate_snake(cls, matrix) -> NormalSnake:
        """Fill matrix body with snake type fields and create snake obj."""
        start_x, start_y = int(matrix.width() / 2), int(matrix.height() / 2)

        matrix.set(BOARD_FIELD_TYPE.SNAKE, start_x, start_y)

        return NormalSnake(start_x, start_y)

    @classmethod
    def _create_fruits(self, matrix) -> typing.List[Coordinates]:
        """Create list of coordinates which represent fruits locations."""
        field_types_allowed_to_overwrite = [BOARD_FIELD_TYPE.GROUND]
        max_fruits_no, min_fruits_no = 3, 1
        max_x_i, max_y_i = matrix.width() - 1, matrix.height() - 1

        desired_fruits_number = randint(min_fruits_no, max_fruits_no)

        results: typing.List[Coordinates] = []

        while len(results) != desired_fruits_number:
            rand_x, rand_y = randint(0, max_x_i), randint(0, max_y_i)

            if any(
                coordinate.x == rand_x and coordinate.y == rand_y
                for coordinate in results
            ):
                continue

            if matrix.get(rand_x, rand_y) not in field_types_allowed_to_overwrite:
                continue

            fruit_coordinates = Coordinates(x=rand_x, y=rand_y)

            results.append(fruit_coordinates)

        return results

    @classmethod
    def _render_fruits(self, matrix, fruits: typing.List[Coordinates]):
        i = 0
        for _ in range(len(fruits)):
            fruit = fruits[i]

            x, y = fruit.x, fruit.y

            fruit_eaten_by_snake = matrix.get(x=x, y=y) == BOARD_FIELD_TYPE.SNAKE

            if fruit_eaten_by_snake:
                fruits.pop(i)
                continue

            i += 1

            matrix.set(x=x, y=y, value=BOARD_FIELD_TYPE.FRUIT)


def generate_board_fields(next_ctx: GAME_MENU_CTX):
    BoardFieldAbs.add_ids_to_children_classes()

    fields = {}

    for sub_class in BoardFieldAbs.__subclasses__():
        new_field = copy(FIELD_TEMPLATE)
        new_field["display_name"] = sub_class.display_name()
        new_field["next_ctx"] = next_ctx

        fields[sub_class.id] = new_field

    if len(fields) == 0:
        raise NotImplementedError("At least one board is required to play.")

    fields[0]["selected"] = True

    return fields


# TO-DO
# create board which has a wall which moves upwords one y/x each n moves
