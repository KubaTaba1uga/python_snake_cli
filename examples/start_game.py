from src.display import BashDisplay
from src.controller import Controller
from src.game_engine.game_engine import GameEngine


def main():
    import shutil

    game_engine = GameEngine()

    controller, display = Controller(game_engine), BashDisplay(game_engine)

    game_engine.start()
    controller.start()
    display.start()

    from time import sleep

    sleep(30)


if __name__ == "__main__":
    main()
