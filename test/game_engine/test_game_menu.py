from src.game_engine.game_menu import GameMenu


def test_game_menu_select_field():
    game_menu, id_to_select = GameMenu(), "create_new_session"

    print(f"{game_menu=} {id_to_select=}")

    game_menu.select_field(id_to_select)

    assert (
        game_menu.fields_map[game_menu.ctx]["fields"][id_to_select]["selected"] is True
    )
