from src.user_input import UserInput
from src.constants import GAME_ENGINE_CTX


class GameEngine:
    DEFAULT_USER_INPUT_VALUE = "None"
    DEFAULT_GAME_ENGINE_CTX = GAME_ENGINE_CTX.MENU

    def __init__(self):
        self.user_input: UserInput = UserInput(self.DEFAULT_USER_INPUT_VALUE)
        self.ctx: GAME_ENGINE_CTX = self.DEFAULT_GAME_ENGINE_CTX
