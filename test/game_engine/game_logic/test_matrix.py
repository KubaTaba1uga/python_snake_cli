import pytest

from src.game_engine.game_logic.matrix import Matrix2D


def test_matrix_init():
    size, expected_result = 5, [
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
        [None, None, None, None, None],
    ]

    matrix = Matrix2D(size, size)

    received_result = matrix._data

    assert received_result == expected_result


@pytest.mark.parametrize(
    "x, y, expected_result", [(0, 1, "Canada"), (2, 2, "Australia"), (4, 4, "Malta")]
)
def test_matrix_get(x, y, expected_result):
    size, matrix_as_list = 5, [
        [None, None, None, None, None],
        ["Canada", None, None, None, None],
        [None, None, "Australia", None, None],
        [None, None, None, None, None],
        [None, None, None, None, "Malta"],
    ]

    matrix = Matrix2D(size, size)
    matrix._data = matrix_as_list

    received_result = matrix.get(x, y)

    assert received_result == expected_result


@pytest.mark.parametrize(
    "x, y, expected_result", [(0, 1, "Canada"), (2, 2, "Australia"), (4, 4, "Malta")]
)
def test_matrix_set(x, y, expected_result):
    size = 5

    matrix = Matrix2D(size, size)
    matrix.set(expected_result, x, y)

    received_result = matrix.get(x, y)

    assert received_result == expected_result


def test_matrix_height():
    size, expected_result = 5, 5

    matrix = Matrix2D(size, size)

    received_result = matrix.height()

    assert received_result == expected_result


def test_matrix_width():
    size, expected_result = 5, 5

    matrix = Matrix2D(size, size)

    received_result = matrix.width()

    assert received_result == expected_result


def test_matrix_cast_to_list():
    size, expected_result = 5, [
        [None, None, None, None, None],
        ["Canada", None, None, None, None],
        [None, None, "Australia", None, None],
        [None, None, None, None, None],
        [None, None, None, None, "Malta"],
    ]

    matrix = Matrix2D(size, size)
    matrix.set("Canada", 0, 1)
    matrix.set("Australia", 2, 2)
    matrix.set("Malta", 4, 4)

    received_result = matrix._data

    assert received_result == expected_result
