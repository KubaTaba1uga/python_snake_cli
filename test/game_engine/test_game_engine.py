import pytest

from src.constants import get_key_value_by_display_name, SnakeDirection
from src.game_engine.session import Session
from src.game_engine.game_engine import GameEngine


@pytest.mark.parametrize(
    "key_value, start_snake_direction, expected_snake_direction",
    [
        pytest.param(
            get_key_value_by_display_name("LEFT ARROW key"),
            SnakeDirection.UP,
            SnakeDirection.LEFT,
            id="left arrow",
        ),
        pytest.param(
            get_key_value_by_display_name("RIGHT ARROW key"),
            SnakeDirection.UP,
            SnakeDirection.RIGHT,
            id="right arrow",
        ),
        pytest.param(
            get_key_value_by_display_name("UP ARROW key"),
            SnakeDirection.LEFT,
            SnakeDirection.UP,
            id="up arrow",
        ),
        pytest.param(
            get_key_value_by_display_name("DOWN ARROW key"),
            SnakeDirection.LEFT,
            SnakeDirection.DOWN,
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
