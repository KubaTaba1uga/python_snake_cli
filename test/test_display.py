from src.constants import GAME_MENU_CTX
from src.display import BashDisplay


def test_bash_display_render_menu_menu(game_engine_menu):
    expected_menu = (
        "\n"
        "\x1b[1K   \x1b[1mGame menu\x1b[0m\x1b[0m\n"
        "\x1b[1K      - \x1b[41mStart New Game\x1b[0\x1b[0m\n"
        "\x1b[1K      - Exit\x1b[0m\n"
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


def test_bash_display_render_menu_show_session(game_engine_menu):
    expected_menu = (
        "\n\x1b[1K   \x1b[1mSession info\x1b[0m\x1b[0m\n"
        "\x1b[1K        start_time: 2011-11-11 00:00:00\x1b[0m\n"
        "\x1b[1K        end_time: 2011-11-11 00:00:01\x1b[0m\n"
        "\x1b[1K        _difficulty_class: <class 'src.game_en"
        "gine.difficulty.DifficultyEasy'>\x1b[0m\n"
        "\x1b[1K        _size_class: <class 'src.game_engine.g"
        "ame_logic.size.SizeSmall'>\x1b[0m\n"
        "\x1b[1K        _board_class: <class 'src.game_engine.g"
        "ame_logic.board.BoardNoWalls'>\x1b[0m\n"
        "\x1b[1K      - \x1b[41mContinue\x1b[0m\x1b[0m\n"
        "\n\n\n\n\n\n\n\n\n\n\n"
    )

    game_engine, terminal_x, terminal_y = game_engine_menu, 300, 20

    game_engine.game_menu._show_session()

    game_engine.game_menu.ctx = GAME_MENU_CTX.SHOW_SESSION

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
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47"
        "m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b["
        "0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[4"
        "7m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b["
        "0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47"
        "m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m"
        " \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
        "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
        "\x1b[0m\x1b[47m \x1b[0m\x1b[44m \x1b[0m\x1b[47m \x1b[0m"
        "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
        "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
        "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
        "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
        "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
        "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
        "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
        "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
        "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
        "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
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
        (
            "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[44m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m"
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
        ),
        (
            "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
            "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
            "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[44m \x1b[0m\x1b[47m \x1b"
            "[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m"
            " \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
            "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
            "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
            "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
            "\n\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m "
            "\x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m\x1b"
            "[47m \x1b[0m\x1b[47m \x1b[0m\x1b[47m \x1b[0m"
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
        ),
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
