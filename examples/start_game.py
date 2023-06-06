from src.display import BashDisplay
from src.controller import Controller
from src.game_engine.game_engine import GameEngine


def main():
    import shutil

    game_engine, terminal_dimmensions = GameEngine(), shutil.get_terminal_size()

    controller, display = Controller(game_engine), BashDisplay(
        game_engine, terminal_dimmensions.columns, terminal_dimmensions.lines
    )

    game_engine.start()
    # controller.start(controller.game_engine)
    # display.start()

    from time import sleep

    sleep(30)


if __name__ == "__main__":
    main()
