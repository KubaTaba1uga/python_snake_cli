import typing
from abc import abstractmethod, ABC
from copy import copy

from src.constants import FIELD_TEMPLATE
from src.constants import GAME_MENU_CTX
from src.game_engine.game_logic.matrix import Matrix2D


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


class BoardAbs(BoardFieldAbs):
    def __init__(self, size: int):
        self.matrix = Matrix2D(size)

        self._initiate_board(self.matrix)

    @classmethod
    @abstractmethod
    def _initiate_board(self, matrix):
        """Fill matrix body with field types."""

    @classmethod
    @abstractmethod
    def _initiate_snake(self, matrix):
        """Fill matrix body with field types."""


class BoardNoWalls(BoardAbs):
    @classmethod
    def display_name(cls) -> str:
        # This is required to generate menu's fields.
        return "No walls"


def generate_board_fields():
    BoardAbs.add_ids_to_children_classes()

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
