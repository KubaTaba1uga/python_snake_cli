from src.constants import BoardFieldType, SnakeDirection
from src.game_engine.game_logic.snake import NormalSnake
from src.game_engine.game_logic.matrix import Matrix2D


def test_normal_snake_move_ground():
    """Place snake on matrix's center. Matrix doesn't have any obstacles."""

    matrix_data, snake, matrix = (
        [
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
        ],
        NormalSnake(2, 2, SnakeDirection.UP),
        Matrix2D(5),
    )

    matrix._data = matrix_data

    snake.move(matrix)

    assert snake.head().x == 2
    assert snake.head().y == 3

    assert snake.tail().x == 2
    assert snake.tail().y == 3
