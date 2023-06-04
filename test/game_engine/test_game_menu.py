from copy import deepcopy

from src.game_engine.game_menu import GameMenu
from src.constants import GAME_MENU_CTX


def test_game_menu_select_field():
    game_menu, id_to_select = GameMenu(), 0

    game_menu.select_field(id_to_select)

    assert (
        game_menu.fields_map[game_menu.ctx]["fields"][id_to_select]["selected"] is True
    )


def test_game_menu_select_field_only_one_allowed():
    game_menu, id_to_select, id_to_unselect = (
        GameMenu(),
        0,
        1,
    )

    fields = game_menu.fields_map[game_menu.ctx]["fields"]

    fields[id_to_unselect]["selected"] = True

    game_menu.select_field(id_to_select)

    assert fields[id_to_select]["selected"] is True
    assert fields[id_to_unselect]["selected"] is False


def test_game_menu_select_next_field_sucess():
    game_menu, selected_id, id_to_select = (
        GameMenu(),
        0,
        1,
    )

    fields = game_menu.fields_map[game_menu.ctx]["fields"]

    fields[selected_id]["selected"] = True

    game_menu.select_next_field()

    assert fields[selected_id]["selected"] is False
    assert fields[id_to_select]["selected"] is True


def test_game_menu_select_previous_field_sucess():
    game_menu, selected_id, id_to_select = (
        GameMenu(),
        1,
        0,
    )

    fields = game_menu.fields_map[game_menu.ctx]["fields"]

    fields[selected_id]["selected"] = True

    game_menu.select_previous_field()

    assert fields[selected_id]["selected"] is False
    assert fields[id_to_select]["selected"] is True


def test_game_menu_select_next_field_out_of_range():
    game_menu, selected_id, id_to_select = (
        GameMenu(),
        1,
        0,
    )

    fields = game_menu.fields_map[game_menu.ctx]["fields"]

    fields[selected_id]["selected"] = True

    game_menu.select_next_field()

    assert fields[selected_id]["selected"] is False
    assert fields[id_to_select]["selected"] is True


def test_game_menu_select_previous_field_out_of_range():
    game_menu, selected_id, id_to_select = (
        GameMenu(),
        0,
        1,
    )

    fields = game_menu.fields_map[game_menu.ctx]["fields"]

    fields[selected_id]["selected"] = True

    game_menu.select_previous_field()

    assert fields[selected_id]["selected"] is False
    assert fields[id_to_select]["selected"] is True


# def test_game_menu_create_new_session():
#     game_menu, selected_id, id_to_select = (
#         GameMenu(),
#         0,
#         1,
#     )

#     game_menu.fields_map[GAME_MENU_CTX.CHOOSE_BOARD]["fields"][0]["selected"] = True
#     game_menu.fields_map[GAME_MENU_CTX.CHOOSE_DIFFICULTY]["fields"][0][
#         "selected"
#     ] = True
#     game_menu.ctx = GAME_MENU_CTX.PLAY_NEW

#     game_menu.process_ctx()
