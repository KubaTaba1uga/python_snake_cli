import pytest

from src.constants import BOARD_FIELD_TYPE
from src.constants import SnakeDirection
from src.errors import SnakeDied
from src.game_engine.game_logic.matrix import Matrix2D
from src.game_engine.game_logic.snake import NormalSnake


def _ground_matrix():
    """Place snake on matrix's center. Matrix doesn't have any obstacles."""

    return [
        [
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
        ],
        [
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
        ],
        [
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.SNAKE,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
        ],
        [
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
        ],
        [
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
            BOARD_FIELD_TYPE.GROUND,
        ],
    ]


def test_normal_snake_move_up():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.UP),
        Matrix2D(5, 5),
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
        Matrix2D(5, 5),
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
        Matrix2D(5, 5),
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
        Matrix2D(5, 5),
    )

    # make snake longer
    snake._grow_head(2, 1)

    matrix._data = matrix_data

    snake.move(matrix)

    assert snake.head().x == 3
    assert snake.head().y == 1

    assert snake.tail().x == 2
    assert snake.tail().y == 1


def test_normal_snake_move_into_wall():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 1, SnakeDirection.RIGHT),
        Matrix2D(5, 5),
    )

    # make snake longer
    snake._grow_head(2, 2)

    matrix._data = matrix_data

    matrix.set(BOARD_FIELD_TYPE.WALL, 3, 2)

    with pytest.raises(SnakeDied):
        snake.move(matrix)


def test_normal_snake_move_into_snake():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(1, 2, SnakeDirection.RIGHT),
        Matrix2D(5, 5),
    )

    # make snake longer
    snake._grow_head(2, 2)

    matrix._data = matrix_data

    matrix.set(BOARD_FIELD_TYPE.SNAKE, 3, 2)

    with pytest.raises(SnakeDied):
        snake.move(matrix)


def test_normal_snake_move_into_fruit():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.RIGHT),
        Matrix2D(5, 5),
    )

    matrix._data = matrix_data

    matrix.set(BOARD_FIELD_TYPE.FRUIT, 3, 2)

    snake.move(matrix)

    assert len(snake) == 2


def test_normal_snake_do_not_turn_around_down():
    org_direction, new_direction = SnakeDirection.UP, SnakeDirection.DOWN

    snake = NormalSnake(2, 2, org_direction)

    snake.set_direction(new_direction)

    assert snake._direction == org_direction


def test_normal_snake_do_not_turn_around_up():
    org_direction, new_direction = SnakeDirection.DOWN, SnakeDirection.UP

    snake = NormalSnake(2, 2, org_direction)

    snake.set_direction(new_direction)

    assert snake._direction == org_direction


def test_normal_snake_do_not_turn_around_left():
    org_direction, new_direction = SnakeDirection.RIGHT, SnakeDirection.LEFT

    snake = NormalSnake(2, 2, org_direction)

    snake.set_direction(new_direction)

    assert snake._direction == org_direction


def test_normal_snake_do_not_turn_around_right():
    org_direction, new_direction = SnakeDirection.LEFT, SnakeDirection.RIGHT

    snake = NormalSnake(2, 2, org_direction)

    snake.set_direction(new_direction)

    assert snake._direction == org_direction


def test_normal_snake_move_show_on_board():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.RIGHT),
        Matrix2D(5, 5),
    )

    matrix._data = matrix_data

    snake.move(matrix)

    assert matrix.get(3, 2) == BOARD_FIELD_TYPE.SNAKE
    assert matrix.get(2, 2) == BOARD_FIELD_TYPE.GROUND


def test_normal_snake_eat_fruit_show_on_board():
    matrix_data, snake, matrix = (
        _ground_matrix(),
        NormalSnake(2, 2, SnakeDirection.RIGHT),
        Matrix2D(5, 5),
    )

    matrix._data = matrix_data
    matrix.set(BOARD_FIELD_TYPE.FRUIT, 3, 2)

    snake.move(matrix)

    assert matrix.get(3, 2) == BOARD_FIELD_TYPE.SNAKE
    assert matrix.get(2, 2) == BOARD_FIELD_TYPE.SNAKE
