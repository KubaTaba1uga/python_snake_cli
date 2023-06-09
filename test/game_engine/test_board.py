from src.constants import BOARD_FIELD_TYPE
from src.constants import GAME_MENU_CTX
from src.game_engine.game_logic.board import Coordinates
from src.game_engine.game_logic.board import generate_board_fields
from src.game_engine.game_logic.matrix import Matrix2D


def test_generate_fields_success(board_no_walls_square):
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


def _ground_matrix(board_no_walls_square):
    """Place snake on matrix's center. Matrix doesn't have any obstacles."""

    matrix_data = [
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

    matrix = Matrix2D(len(matrix_data))
    matrix._data = matrix_data
    return matrix


def test_board_no_walls_create_fruits(board_no_walls_square):
    max_fruits_no, min_fruits_no = 3, 1

    board = board_no_walls_square
    matrix = board.matrix

    received_fruits = board._create_fruits(matrix)

    assert min_fruits_no <= len(received_fruits) <= max_fruits_no

    for fruit_coordinates in received_fruits:
        assert fruit_coordinates.x < matrix.width()
        assert fruit_coordinates.y < matrix.height()


def test_board_no_walls_render_fruits_simple(board_no_walls_square):
    board = board_no_walls_square
    matrix = board.matrix

    fruits = [Coordinates(1, 2), Coordinates(3, 4), Coordinates(4, 3)]

    board._render_fruits(matrix, fruits)

    for fruit in fruits:
        assert matrix.get(fruit.x, fruit.y) == BOARD_FIELD_TYPE.FRUIT


def test_board_no_walls_render_fruits_eaten_by_snake(board_no_walls_square):
    board = board_no_walls_square
    matrix = board.matrix

    fruits = [Coordinates(1, 2), Coordinates(2, 2), Coordinates(2, 3)]

    board._render_fruits(matrix, fruits)

    assert len(fruits) == 2


def test_board_no_walls_process_simple(board_no_walls_square):
    board = board_no_walls_square

    board.process()

    snake_head = board.snake.head()

    assert snake_head.x == 2
    assert snake_head.y == 1

    assert board.matrix.get(snake_head.x, snake_head.y) == BOARD_FIELD_TYPE.SNAKE


def test_board_no_walls_process_fruit(board_no_walls_square):
    board, fruit = board_no_walls_square, Coordinates(2, 1)

    board.fruits = [fruit]
    board.matrix.set(BOARD_FIELD_TYPE.FRUIT, fruit.x, fruit.y)

    board.process()

    snake_head, snake_tail = board.snake.head(), board.snake.tail()

    assert snake_head.x == 2
    assert snake_head.y == 1
    assert snake_tail.x == 2
    assert snake_tail.y == 2

    assert board.matrix.get(snake_head.x, snake_head.y) == BOARD_FIELD_TYPE.SNAKE
    assert board.matrix.get(snake_tail.x, snake_tail.y) == BOARD_FIELD_TYPE.SNAKE

    board.process()
    board.process()
    assert board.fruits[0] is not fruit
