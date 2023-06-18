from datetime import datetime

import pytest

from src.constants import GAME_ENGINE_CTX
from src.game_engine.difficulty import DifficultyEasy
from src.game_engine.game_engine import GameEngine
from src.game_engine.game_logic.board import BoardNoWalls
from src.game_engine.game_logic.size import SizeSmall
from src.game_engine.session import Session


@pytest.fixture
def game_engine_menu(session_small_board_no_walls_easy):
    game_engine = GameEngine()
    game_engine.ctx = GAME_ENGINE_CTX.MENU

    game_engine.game_menu.session = session_small_board_no_walls_easy

    return game_engine


@pytest.fixture
def game_engine_game(session_small_board_no_walls_easy_not_finished):
    game_engine = GameEngine()
    game_engine.ctx = GAME_ENGINE_CTX.GAME

    game_engine.game_menu.session = session_small_board_no_walls_easy_not_finished

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


@pytest.fixture
def session_small_board_no_walls_easy_not_finished():
    session = Session(
        difficulty_class=DifficultyEasy, board_class=BoardNoWalls, size_class=SizeSmall
    )

    session.start_time = datetime.fromisoformat("2011-11-11T00:00:00")

    return session
