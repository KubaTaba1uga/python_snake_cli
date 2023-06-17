from datetime import datetime

import pytest


from src.constants import GAME_MENU_CTX
from src.game_engine.session import SessionDummy, generate_session_fields


def test_dummy_session():
    session = SessionDummy()

    with pytest.raises(NotImplementedError):
        session.board


def test_generate_session_fields(session_small_board_no_walls_easy):
    session, expected_value = session_small_board_no_walls_easy, {
        0: {
            "display_name": f"start_time: {datetime.fromisoformat('2011-11-11T00:00:00')}",
            "selected": True,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": False,
        },
        1: {
            "display_name": f"end_time: {datetime.fromisoformat('2011-11-11T00:00:01')}",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": False,
        },
        2: {
            "display_name": "_difficulty_class: <class 'src.game_engine.difficulty.DifficultyEasy'>",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": False,
        },
        3: {
            "display_name": "_size_class: <class 'src.game_engine.game_logic.size.SizeSmall'>",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": False,
        },
        4: {
            "display_name": "_board_class: <class 'src.game_engine.game_logic.board.BoardNoWalls'>",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": False,
        },
    }

    received_value = generate_session_fields(session)

    assert received_value == expected_value
