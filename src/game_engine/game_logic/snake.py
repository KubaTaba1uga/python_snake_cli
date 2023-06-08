import typing
from abc import ABC
from dataclasses import dataclass


@dataclass
class SnakeBody:
    """Part of the snake.
    It represents board's field.
    x - width, y - height."""

    x: int
    y: int


class SnakeAbs(ABC):
    def __init__(self):
        self.body: typing.List[SnakeBody] = []

    def head(self):
        if len(self.body) == 0:
            raise
