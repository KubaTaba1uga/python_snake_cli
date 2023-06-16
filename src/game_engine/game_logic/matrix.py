import typing


class Matrix2D:
    """Two dimmensional matrix."""

    def __init__(
        self,
        height: int,
        width: int,
    ):
        if height < 1 or width < 1:
            raise ValueError(height, width)

        self._data: typing.List[typing.List] = self._create_column(height, width)

    @classmethod
    def _create_column(cls, height: int, width) -> typing.List[typing.List[None]]:
        return [cls._create_row(width) for _ in range(height)]

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
