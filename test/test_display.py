from src.display import BashDisplay


from test.conftest import game_engine as _game_engine


def test_bash_display_render_menu():
    expected_menu = (
        "   \x1b[1mGame menu\x1b[0m\n   "
        "   - \x1b[41mStart New Game\x1b[0m\n   "
        "   - Save Current Game\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = _game_engine(), 30, 20

    received_menu = BashDisplay.render_game_menu(game_engine, terminal_x, terminal_y)

    assert received_menu == expected_menu
