import pytest

from src.constants import BoardFieldType, SnakeDirection
from src.game_engine.game_logic.snake import NormalSnake
from src.game_engine.game_logic.matrix import Matrix2D


def _ground_matrix():
    """Place snake on matrix's center. Matrix doesn't have any obstacles."""

    return [
        [
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
        ],
        [
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
        ],
        [
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.SNAKE,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
        ],
        [
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
        ],
        [
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
            BoardFieldType.GROUND,
        ],
    ]


def test_normal_snake_move_up():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.UP),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(3, 2)

    matrix._data = matrix_data

    snake.move(matrix)

    assert snake.head().x == 3
    assert snake.head().y == 1

    assert snake.tail().x == 3
    assert snake.tail().y == 2


def test_normal_snake_move_down():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.DOWN),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(3, 2)

    matrix._data = matrix_data

    snake.move(matrix)

    assert snake.head().x == 3
    assert snake.head().y == 3

    assert snake.tail().x == 3
    assert snake.tail().y == 2


def test_normal_snake_move_left():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.LEFT),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(1, 2)

    matrix._data = matrix_data

    snake.move(matrix)

    assert snake.head().x == 0
    assert snake.head().y == 2

    assert snake.tail().x == 1
    assert snake.tail().y == 2


def test_normal_snake_move_right():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.RIGHT),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(2, 1)

    matrix._data = matrix_data

    snake.move(matrix)

    assert snake.head().x == 3
    assert snake.head().y == 1

    assert snake.tail().x == 2
    assert snake.tail().y == 1


def test_normal_snake_do_not_turn_around_down():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.RIGHT),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(2, 1)

    matrix._data = matrix_data

    with pytest.raises(ValueError):
        snake.set_direction(SnakeDirection.DOWN)


def test_normal_snake_do_not_turn_around_up():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.RIGHT),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(2, 3)

    matrix._data = matrix_data

    with pytest.raises(ValueError):
        snake.set_direction(SnakeDirection.UP)


def test_normal_snake_do_not_turn_around_left():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.UP),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(3, 2)

    matrix._data = matrix_data

    with pytest.raises(ValueError):
        snake.set_direction(SnakeDirection.LEFT)


def test_normal_snake_do_not_turn_around_right():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.UP),
        Matrix2D(5),
    )

    # make snake longer
    snake._grow_head(1, 2)

    matrix._data = matrix_data

    with pytest.raises(ValueError):
        snake.set_direction(SnakeDirection.RIGHT)
