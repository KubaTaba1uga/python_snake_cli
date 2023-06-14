from src.constants import BoardFieldType
from src.constants import GAME_MENU_CTX
from src.game_engine.game_logic.board import BoardNoWalls
from src.game_engine.game_logic.board import Coordinates
from src.game_engine.game_logic.board import generate_board_fields
from src.game_engine.game_logic.matrix import Matrix2D


def test_generate_fields_success():
    expected_results = {
        0: {
            "display_name": "No walls",
            "selected": True,
            "next_ctx": GAME_MENU_CTX.CHOOSE_DIFFICULTY,
            "disabled": False,
        }
    }

    received_results = generate_board_fields(GAME_MENU_CTX.CHOOSE_DIFFICULTY)

    assert received_results == expected_results


def _ground_matrix():
    """Place snake on matrix's center. Matrix doesn't have any obstacles."""

    matrix_data = [
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

    matrix = Matrix2D(len(matrix_data))
    matrix._data = matrix_data
    return matrix


def _no_walls_board():
    return BoardNoWalls(5, 5)


def test_board_no_walls_create_fruits():
    max_fruits_no, min_fruits_no = 3, 1

    board = _no_walls_board()
    matrix = board.matrix

    received_fruits = board._create_fruits(matrix)

    assert min_fruits_no <= len(received_fruits) <= max_fruits_no

    for fruit_coordinates in received_fruits:
        assert fruit_coordinates.x < matrix.width()
        assert fruit_coordinates.y < matrix.height()


def test_board_no_walls_render_fruits_simple():
    board = _no_walls_board()
    matrix = board.matrix

    fruits = [Coordinates(1, 2), Coordinates(3, 4), Coordinates(4, 3)]

    board._render_fruits(matrix, fruits)

    for fruit in fruits:
        assert matrix.get(fruit.x, fruit.y) == BoardFieldType.FRUIT


def test_board_no_walls_render_fruits_eaten_by_snake():
    board = _no_walls_board()
    matrix = board.matrix

    fruits = [Coordinates(1, 2), Coordinates(2, 2), Coordinates(2, 3)]

    board._render_fruits(matrix, fruits)

    assert len(fruits) == 2


def test_board_no_walls_process_simple():
    board = _no_walls_board()

    board.process()

    snake_head = board.snake.head()

    assert snake_head.x == 2
    assert snake_head.y == 1

    assert board.matrix.get(snake_head.x, snake_head.y) == BoardFieldType.SNAKE


def test_board_no_walls_process_fruit():
    board, fruit = _no_walls_board(), Coordinates(2, 1)

    board.fruits = [fruit]
    board.matrix.set(BoardFieldType.FRUIT, fruit.x, fruit.y)

    board.process()

    snake_head, snake_tail = board.snake.head(), board.snake.tail()

    assert snake_head.x == 2
    assert snake_head.y == 1
    assert snake_tail.x == 2
    assert snake_tail.y == 2

    assert board.matrix.get(snake_head.x, snake_head.y) == BoardFieldType.SNAKE
    assert board.matrix.get(snake_tail.x, snake_tail.y) == BoardFieldType.SNAKE

    board.process()

    assert board.fruits[0] is not fruit
