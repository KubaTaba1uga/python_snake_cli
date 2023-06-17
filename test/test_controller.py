from pynput import keyboard as _keyboard

from src.controller import Controller


def simulate_key_press(key):
    keyboard = _keyboard.Controller()
    keyboard.press(key)
    keyboard.release(key)


def test_controller_thread_is_not_active(game_engine_menu):
    game_engine = game_engine_menu
    controller = Controller(game_engine)

    controller.start()

    controller.stop()

    assert controller.is_active() is False


def test_controller_thread_is_active(game_engine_menu):
    game_engine = game_engine_menu
    controller = Controller(game_engine)

    controller.start()

    try:
        assert controller.is_active() is True
    finally:
        controller.stop()


def test_controller_ctx_manager(game_engine_menu):
    game_engine = game_engine_menu
    controller = Controller(game_engine)

    with controller:
        pass

    assert controller.is_active() is False


def test_controller_unrecognizable_key(game_engine_menu):
    unrecognizable_key, expected_value = _keyboard.Key.ctrl, "foo"

    game_engine, controller = game_engine_menu, Controller

    game_engine.user_input.set(expected_value)

    with controller(game_engine):
        simulate_key_press(unrecognizable_key)

    assert game_engine.user_input.get() == expected_value


def test_controller_recognizable_key(game_engine_menu):
    unrecognizable_key, expected_value = _keyboard.Key.esc, "escape"

    game_engine, controller = game_engine_menu, Controller

    game_engine.user_input.set(expected_value)

    with controller(game_engine):
        simulate_key_press(unrecognizable_key)

    assert game_engine.user_input.get() == expected_value
