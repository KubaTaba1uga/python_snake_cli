from test.conftest import game_engine as GameEngine

from pynput import keyboard as _keyboard

from src.controller import Controller


def simulate_key_press(key):
    keyboard = _keyboard.Controller()
    keyboard.press(key)
    keyboard.release(key)


def test_controller_thread_is_not_active():
    game_engine, controller = GameEngine(), Controller

    controller.start(game_engine)

    controller.stop()

    assert controller.is_active() is False

    controller.cleanup()


def test_controller_thread_is_active():
    game_engine, controller = GameEngine(), Controller

    controller.start(game_engine)

    try:
        assert controller.is_active() is True
    finally:
        controller.stop()
        controller.cleanup()


def test_controller_ctx_manager():
    game_engine, controller = GameEngine(), Controller

    with controller(game_engine):
        pass

    assert controller._does_thread_exsists() is False


def test_controller_unrecognizable_key():
    unrecognizable_key, expected_value = _keyboard.Key.ctrl, "foo"

    game_engine, controller = GameEngine(), Controller

    game_engine.user_input.set(expected_value)

    with controller(game_engine):
        simulate_key_press(unrecognizable_key)

    assert game_engine.user_input.get() == expected_value


def test_controller_recognizable_key():
    unrecognizable_key, expected_value = _keyboard.Key.esc, "escape"

    game_engine, controller = GameEngine(), Controller

    game_engine.user_input.set(expected_value)

    with controller(game_engine):
        simulate_key_press(unrecognizable_key)

    assert game_engine.user_input.get() == expected_value
