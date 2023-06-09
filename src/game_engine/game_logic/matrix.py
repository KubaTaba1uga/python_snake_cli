import typing
import copy


class Matrix2D:
    """ Fixed size two dimmensional array."""

    def __init__(self, size: int):
        if size < 1:
            raise ValueError(size)

        self._data: typing.List[typing.List] = self._create_column(size)

    @classmethod
    def _create_column(cls, size: int) -> typing.List[typing.List[None]]:
        return [cls._create_row(size) for _ in range(size)]

    @classmethod
    def _create_row(cls, size: int) -> typing.List[None]:
        return [None for _ in range(size)]

    def get(self, x: int, y: int) -> typing.Any:
        return self._data[y][x]

    def set(self, value: typing.Any, x: int, y: int):
        self._data[y][x] = value

    def height(self) -> int:
        return len(self._data)

    def width(self) -> int:
        return len(self._data[0])

    def cast_to_list(self) -> typing.List[typing.List[typing.Any]]:
        return [[value for value in nested_l] for nested_l in self._data]
