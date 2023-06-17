import pytest

from src.constants import get_key_value_by_display_name
from src.constants import SNAKE_DIRECTION


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
