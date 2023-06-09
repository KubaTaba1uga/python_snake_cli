import typing
from abc import ABC
from abc import abstractmethod
from copy import copy

from src.constants import FIELD_TEMPLATE
from src.constants import GAME_MENU_CTX


class SizeFieldAbs(ABC):
    # Id is required by Menu, to link field with size.
    id: typing.Optional[int] = None

    @classmethod
    @abstractmethod
    def display_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def add_ids_to_children_classes(cls):
        for i, sub_class in enumerate(cls.__subclasses__()):
            sub_class.id = i

    @classmethod
    def get_children_class_by_id(cls, id_):
        for sub_class in cls.__subclasses__():
            if sub_class.id == id_:
                return sub_class

        raise NotImplementedError(cls, id_)


class SizeAbs(ABC):
    @classmethod
    @abstractmethod
    def width(cls) -> int:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def height(cls) -> int:
        raise NotImplementedError()


class SizeSmall(SizeAbs, SizeFieldAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Small"

    @classmethod
    def width(cls) -> int:
        return 10

    @classmethod
    def height(cls) -> int:
        return 10


class SizeMedium(SizeAbs, SizeFieldAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Medium"

    @classmethod
    def width(cls) -> int:
        return 25

    @classmethod
    def height(cls) -> int:
        return 25


class SizeBig(SizeAbs, SizeFieldAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Big"

    @classmethod
    def width(cls) -> int:
        return 50

    @classmethod
    def height(cls) -> int:
        return 50


class SizeLarge(SizeAbs, SizeFieldAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Large"

    @classmethod
    def width(cls) -> int:
        return 100

    @classmethod
    def height(cls) -> int:
        return 50


def generate_size_fields(next_ctx: GAME_MENU_CTX):
    SizeFieldAbs.add_ids_to_children_classes()

    fields = {}

    for sub_class in SizeFieldAbs.__subclasses__():
        new_field = copy(FIELD_TEMPLATE)
        new_field["display_name"] = sub_class.display_name()
        new_field["next_ctx"] = next_ctx

        fields[sub_class.id] = new_field

    if len(fields) == 0:
        raise NotImplementedError("At least one size is required to play.")

    fields[0]["selected"] = True

    return fields
