from src.game_engine.game_menu import GameMenu


def test_game_menu_select_field():
    game_menu, id_to_select = GameMenu(), "1"

    game_menu.select_field(id_to_select)

    assert game_menu[GameMenu.ctx]["fields"][id_to_select]["selected"] is True
