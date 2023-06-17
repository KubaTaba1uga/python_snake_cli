from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.constants import GAME_ENGINE_CTX
from src.game_engine.difficulty import DifficultyEasy
from src.game_engine.game_engine import GameEngine
from src.game_engine.game_logic.board import BoardNoWalls
from src.game_engine.game_logic.size import SizeSmall
from src.game_engine.session import Session


@pytest.fixture
def game_engine_menu():
    game_engine = GameEngine()
    game_engine.ctx = GAME_ENGINE_CTX.MENU

    return game_engine


@pytest.fixture
def game_engine_game():
    game_engine = GameEngine()
    game_engine.ctx = GAME_ENGINE_CTX.GAME

    board = BoardNoWalls(width=5, height=5)

    session = MagicMock(board=board)

    game_engine._session = session

    return game_engine


@pytest.fixture
def board_no_walls_square():
    return BoardNoWalls(5, 5)


@pytest.fixture
def board_no_walls_rect():
    return BoardNoWalls(10, 5)


@pytest.fixture
def session_small_board_no_walls_easy():
    session = Session(
        difficulty_class=DifficultyEasy, board_class=BoardNoWalls, size_class=SizeSmall
    )

    session.start_time = datetime.fromisoformat("2011-11-11T00:00:00")
    session.end_time = datetime.fromisoformat("2011-11-11T00:00:01")

    return session
