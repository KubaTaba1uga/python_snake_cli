from src.game_engine.game_menu import GameMenu


def test_game_menu_select_field():
    game_menu, id_to_select = GameMenu(), "create_new_session"

    game_menu.select_field(id_to_select)

    assert (
        game_menu.fields_map[game_menu.ctx]["fields"][id_to_select]["selected"] is True
    )


def test_game_menu_select_field_only_one_allowed():
    game_menu, id_to_select, id_to_unselect = (
        GameMenu(),
        "create_new_session",
        "save_current_session",
    )

    fields = game_menu.fields_map[game_menu.ctx]["fields"]

    fields[id_to_unselect]["selected"] = True

    game_menu.select_field(id_to_select)

    assert fields[id_to_select]["selected"] is True
    assert fields[id_to_unselect]["selected"] is False
