""" This is only conftest file in tests. Please do not
create a new ones, all fixtures should be available for all tests.
"""

from src.game_engine.game_engine import GameEngine


def game_engine():
    return GameEngine()
