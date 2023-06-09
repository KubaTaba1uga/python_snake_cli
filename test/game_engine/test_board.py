from src.constants import GAME_MENU_CTX, BoardFieldType
from src.game_engine.game_logic.board import generate_board_fields
from src.game_engine.game_logic.board import BoardNoWalls
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

    received_results = generate_board_fields()

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


def test_board_no_walls_create_fruits():
    max_fruits_no, min_fruits_no = 3, 1

    matrix = _ground_matrix()

    received_fruits = BoardNoWalls._create_fruits(matrix)

    assert min_fruits_no <= len(received_fruits) <= max_fruits_no

    for fruit_coordinates in received_fruits:
        assert fruit_coordinates.x < matrix.width()
        assert fruit_coordinates.y < matrix.height()
