from time import sleep

from src.game_engine.game_engine import GameEngine
from src.controller import Controller

if __name__ == "__main__":
    sleep(2)

    ge = GameEngine()
    Controller.start(ge)

    sleep(30)

    print(ge.user_input.get())
