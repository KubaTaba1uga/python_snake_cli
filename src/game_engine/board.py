import typing
from abc import abstractmethod
from copy import copy

from src.constants import FIELD_TEMPLATE
from src.constants import GAME_MENU_CTX


class BoardAbs:
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


class BoardNoWalls(BoardAbs):
    @classmethod
    def display_name(cls) -> str:
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
