from copy import copy
from abc import abstractclassmethod, abstractproperty

from src.constants import FIELD_TEMPLATE, GAME_MENU_CTX


class DifficultyAbs:
    id: int = -1

    @abstractclassmethod
    def display_name(cls) -> str:
        raise NotImplementedError()

    @classmethod
    def add_ids_to_children_classes(cls):
        """ Ids are required by Menu, to reognize which field is seleted. """
        for i, sub_class in enumerate(cls.__subclasses__()):
            sub_class.id = i


class DifficultyEasy(DifficultyAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Easy"


class DifficultyMedium(DifficultyAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Medium"


class DifficultyHard(DifficultyAbs):
    @classmethod
    def display_name(cls) -> str:
        return "Hard"


def generate_difficulty_fields():
    DifficultyAbs.add_ids_to_children_classes()

    fields, next_ctx = {}, GAME_MENU_CTX.CHOOSE_DIFFICULTY

    for sub_class in DifficultyAbs.__subclasses__():
        new_field = copy(FIELD_TEMPLATE)
        new_field["display_name"] = sub_class.display_name()
        new_field["next_ctx"] = next_ctx

        fields[sub_class.id] = new_field

    if len(fields) == 0:
        raise NotImplementedError("At least one difficulty is required to play.")

    fields[0]["selected"] = True

    return fields
