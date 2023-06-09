from src.constants import GAME_MENU_CTX
from src.game_engine.difficulty import generate_difficulty_fields


def test_generate_fields_success():
    expected_results = {
        0: {
            "disabled": False,
            "display_name": "Easy",
            "next_ctx": GAME_MENU_CTX.PLAY_NEW,
            "selected": True,
        },
        1: {
            "disabled": False,
            "display_name": "Medium",
            "next_ctx": GAME_MENU_CTX.PLAY_NEW,
            "selected": False,
        },
        2: {
            "disabled": False,
            "display_name": "Hard",
            "next_ctx": GAME_MENU_CTX.PLAY_NEW,
            "selected": False,
        },
    }

    received_results = generate_difficulty_fields(GAME_MENU_CTX.PLAY_NEW)

    assert received_results == expected_results
