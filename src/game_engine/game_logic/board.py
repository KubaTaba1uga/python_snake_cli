import typing
from abc import ABC
from abc import abstractmethod
from copy import copy
from dataclasses import dataclass
from random import randint

from src.constants import BoardFieldType
from src.constants import FIELD_TEMPLATE
from src.constants import GAME_MENU_CTX
from src.game_engine.game_logic.matrix import Matrix2D
from src.game_engine.game_logic.snake import NormalSnake
from src.game_engine.game_logic.snake import SnakeAbs


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
    def __init__(self, size: int):
        self.matrix = Matrix2D(size)

        self._initiate_board_basic(self.matrix)

        self.snake: SnakeAbs = self._initiate_snake(self.matrix)

        self.create_fruits()

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self.matrix.width(), self.matrix.height()

    def process(self):
        self._render_fruits(self.matrix, self.fruits)

        if self.are_fruits_empty:
            self.create_fruits()

        self.move_snake()

    @property
    def are_fruits_empty(self) -> bool:
        return len(self.fruits) == 0

    def create_fruits(self):
        self.fruits = self._create_fruits(self.matrix)

    def move_snake(self):
        self.snake.move(self.matrix)

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
                matrix.set(BoardFieldType.GROUND, x, y)

    @classmethod
    def _initiate_snake(cls, matrix) -> NormalSnake:
        """Fill matrix body with snake type fields and create snake obj."""
        start_x, start_y = int(matrix.width() / 2), int(matrix.height() / 2)

        matrix.set(BoardFieldType.SNAKE, start_x, start_y)

        return NormalSnake(start_x, start_y)

    @classmethod
    def _create_fruits(self, matrix) -> typing.List[Coordinates]:
        """Create list of coordinates which represent fruits locations."""
        field_types_allowed_to_overwrite = [BoardFieldType.GROUND]
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

            fruit_eaten_by_snake = matrix.get(x=x, y=y) == BoardFieldType.SNAKE

            if fruit_eaten_by_snake:
                fruits.pop(i)
                continue

            i += 1

            matrix.set(x=x, y=y, value=BoardFieldType.FRUIT)


def generate_board_fields():
    BoardFieldAbs.add_ids_to_children_classes()

    fields, next_ctx = {}, GAME_MENU_CTX.CHOOSE_DIFFICULTY

    for sub_class in BoardAbs.__subclasses__():
        new_field = copy(FIELD_TEMPLATE)
        new_field["display_name"] = sub_class.display_name()
        new_field["next_ctx"] = next_ctx

        fields[sub_class.id] = new_field

    if len(fields) == 0:
        raise NotImplementedError("At least one board is required to play.")

    fields[0]["selected"] = True

    return fields


# TO-DO
# create board which moves upwords one y/x each 5 moves
