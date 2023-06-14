# def test_game_engine_set_direction_left():
#     expected_matrix, expected_snake_body = (), ()

#     game_engine, board, terminal_x, terminal_y = _game_engine(), BoardNoWalls(5), 30, 20

#     session = MagicMock(board=board)

#     # game_engine.board = board

#     display = BashDisplay(game_engine)
#     with patch.object(display._game_engine, "_session", session):
#         received_menu = display.render_game_engine(game_engine, terminal_x, terminal_y)

#     assert received_menu == expected_screen
