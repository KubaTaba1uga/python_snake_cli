from src.game_engine.board import generate_board_fields

from src.constants import GAME_MENU_CTX


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
