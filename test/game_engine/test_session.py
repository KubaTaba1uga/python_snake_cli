from datetime import datetime
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.constants import GAME_MENU_CTX
from src.game_engine.session import generate_session_fields
from src.game_engine.session import SessionDummy


def test_dummy_session():
    session = SessionDummy()

    with pytest.raises(NotImplementedError):
        session.board


def test_generate_session_fields(session_small_board_no_walls_easy):
    session, expected_value = session_small_board_no_walls_easy, {
        0: {
            "display_name": f"start_time: {datetime.fromisoformat('2011-11-11T00:00:00')}",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": True,
        },
        1: {
            "display_name": f"end_time: {datetime.fromisoformat('2011-11-11T00:00:01')}",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": True,
        },
        2: {
            "display_name": "_difficulty_class: <class 'src.game_engine.difficulty.DifficultyEasy'>",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": True,
        },
        3: {
            "display_name": "_size_class: <class 'src.game_engine.game_logic.size.SizeSmall'>",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": True,
        },
        4: {
            "display_name": "_board_class: <class 'src.game_engine.game_logic.board.BoardNoWalls'>",
            "selected": False,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": True,
        },
        5: {
            "display_name": "Continue",
            "selected": True,
            "next_ctx": GAME_MENU_CTX.MENU,
            "disabled": False,
        },
    }

    received_value = generate_session_fields(session)

    assert received_value == expected_value


def test_session_finish(session_small_board_no_walls_easy_not_finished):
    session = session_small_board_no_walls_easy_not_finished

    expected_value = datetime.fromisoformat("2011-11-11T00:00:00")

    datetime_local = MagicMock(now=lambda: expected_value)

    with patch("src.game_engine.session.datetime", datetime_local):
        session.finish()

    assert session.end_time is not None
    assert session.end_time == expected_value
