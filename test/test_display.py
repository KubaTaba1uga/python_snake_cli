from unittest.mock import MagicMock
from unittest.mock import patch

from src.constants import GAME_MENU_CTX
from src.display import BashDisplay
from src.game_engine.game_logic.board import BoardNoWalls


def test_bash_display_render_menu_menu(game_engine_menu):
    expected_menu = (
        "\n"
        "\x1b[1K   \x1b[1mGame menu\x1b[0m\x1b[0m\n"
        "\x1b[1K      - \x1b[41mStart New Game\x1b[0\x1b[0m\n"
        "\x1b[1K      - Save Current Game\x1b[0m\n"
        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = game_engine_menu, 30, 20

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_menu_choose_board(game_engine_menu):
    expected_menu = (
        "\n\x1b[1K   \x1b[1mBoard choice\x1b[0m\x1b[0m\n"
        "\x1b[1K      - \x1b[41mNo walls\x1b[0m\x1b[0m\n"
        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = game_engine_menu, 30, 20

    game_engine.game_menu.ctx = GAME_MENU_CTX.CHOOSE_BOARD

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_menu_choose_difficulty(game_engine_menu):
    expected_menu = (
        "\n"
        "\x1b[1K   \x1b[1mDifficulty choice\x1b[0m\x1b[0m\n"
        "\x1b[1K      - \x1b[41mEasy\x1b[0m\x1b[0m\n"
        "\x1b[1K      - Medium\x1b[0m\n"
        "\x1b[1K      - Hard\x1b[0m\n"
        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = game_engine_menu, 30, 20

    game_engine.game_menu.ctx = GAME_MENU_CTX.CHOOSE_DIFFICULTY

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_menu_waiting_screen(game_engine_menu):
    expected_menu = (
        "\n"
        "\x1b[1K   \x1b[1mGame is loading...\x1b[0m\x1b[0m\n"
        "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = game_engine_menu, 30, 20

    game_engine.game_menu.ctx = GAME_MENU_CTX.PLAY_NEW

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_engine_init(game_engine_game):
    expected_screen = (
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[44m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
    )

    game_engine, terminal_x, terminal_y = (
        game_engine_game,
        30,
        20,
    )

    display = BashDisplay(game_engine)

    received_screen = display.render_game_engine(game_engine, terminal_x, terminal_y)

    assert received_screen == expected_screen


def test_bash_display_render_engine_snake_moves(game_engine_game):
    expected_screen_before_move, expected_screen_after_move = (
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[44m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
    ), (
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[44m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
        "\n"
    )

    game_engine, terminal_x, terminal_y = (
        game_engine_game,
        30,
        20,
    )

    display = BashDisplay(game_engine)

    received_screen_before_move = display.render_game_engine(
        game_engine, terminal_x, terminal_y
    )

    game_engine.board.move_snake()

    received_screen_after_move = display.render_game_engine(
        game_engine, terminal_x, terminal_y
    )

    assert received_screen_before_move == expected_screen_before_move
    assert received_screen_after_move == expected_screen_after_move
