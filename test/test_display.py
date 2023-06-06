from src.display import BashDisplay


from test.conftest import game_engine as _game_engine


def test_bash_display_render_menu_menu():
    expected_menu = (
        "   \x1b[1mGame menu\x1b[0m\n   "
        "   - \x1b[41mStart New Game\x1b[0m\n   "
        "   - Save Current Game\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = _game_engine(), 30, 20

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_menu_choose_board():
    expected_menu = (
        "   \x1b[1mBoard choice\x1b[0m\n     "
        " - \x1b[41mNo walls\x1b[0m\n\n\n\n\n"
        "\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = _game_engine(), 30, 20

    game_engine.game_menu.set_new_ctx()

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_menu_choose_difficulty():
    expected_menu = (
        "   \x1b[1mDifficulty choice\x1b[0m\n   "
        "   - \x1b[41mEasy\x1b[0m\n   "
        "   - Medium\n   "
        "   - Hard\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = _game_engine(), 30, 20

    # Go to choose board
    game_engine.game_menu.set_new_ctx()
    # Go to choose difficulty
    game_engine.game_menu.set_new_ctx()
    # # Go to new game
    # game_engine.game_menu.set_new_ctx()

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu


def test_bash_display_render_menu_waiting_screen():
    expected_menu = (
        "   \x1b[1m\x1b[0m\n      "
        "- Game is loading ...\n\n"
        "\n\n\n\n\n\n\n\n\n\n\n\n\n"
        "\n\n"
    )

    game_engine, terminal_x, terminal_y = _game_engine(), 30, 20

    # Go to choose board
    game_engine.game_menu.set_new_ctx()
    # Go to choose difficulty
    game_engine.game_menu.set_new_ctx()
    # # Go to new game
    game_engine.game_menu.set_new_ctx()

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu