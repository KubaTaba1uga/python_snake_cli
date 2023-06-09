from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from src.constants import GAME_ENGINE_CTX
from src.constants import get_key_value_by_display_name
from src.constants import SNAKE_DIRECTION
from src.errors import SnakeDied


@pytest.mark.parametrize(
    "key_value, start_snake_direction, expected_snake_direction",
    [
        pytest.param(
            get_key_value_by_display_name("LEFT ARROW key"),
            SNAKE_DIRECTION.UP,
            SNAKE_DIRECTION.LEFT,
            id="left arrow",
        ),
        pytest.param(
            get_key_value_by_display_name("RIGHT ARROW key"),
            SNAKE_DIRECTION.UP,
            SNAKE_DIRECTION.RIGHT,
            id="right arrow",
        ),
        pytest.param(
            get_key_value_by_display_name("UP ARROW key"),
            SNAKE_DIRECTION.LEFT,
            SNAKE_DIRECTION.UP,
            id="up arrow",
        ),
        pytest.param(
            get_key_value_by_display_name("DOWN ARROW key"),
            SNAKE_DIRECTION.LEFT,
            SNAKE_DIRECTION.DOWN,
            id="down arrow",
        ),
    ],
)
def test_game_engine_process_user_input(
    game_engine_game, key_value, start_snake_direction, expected_snake_direction
):
    game_engine, key_value = game_engine_game, key_value

    game_engine.board.snake._direction = start_snake_direction

    game_engine.user_input.set(key_value)

    game_engine._process_user_input()

    received_snake_direction = game_engine.board.snake._direction

    assert received_snake_direction == expected_snake_direction


def test_game_engine_show_menu_if_snake_dead(game_engine_game):
    game_engine = game_engine_game

    def kill_snake():
        raise SnakeDied("")

    snake_mock = MagicMock(process=kill_snake)

    with patch("src.game_engine.game_engine.GameEngine.board", snake_mock):
        with patch("src.game_engine.game_engine.sleep", lambda _: None):
            game_engine._process_ctx()

    assert game_engine.session.is_finished() is True
    assert game_engine.ctx == GAME_ENGINE_CTX.MENU


def test_game_engine_pause(game_engine_game):
    game_engine = game_engine_game
    game_engine.ctx = GAME_ENGINE_CTX.GAME

    game_engine.user_input.set(get_key_value_by_display_name("p key"))

    game_engine._process()

    assert game_engine.ctx == GAME_ENGINE_CTX.PAUSE


def test_game_engine_unpause(game_engine_game):
    game_engine = game_engine_game
    game_engine.ctx = GAME_ENGINE_CTX.PAUSE

    game_engine.user_input.set(get_key_value_by_display_name("p key"))

    game_engine._process()

    assert game_engine.ctx == GAME_ENGINE_CTX.GAME
