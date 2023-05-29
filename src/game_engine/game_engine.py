from src.user_input import UserInput


class GameEngine:
    DEFAULT_USER_INPUT_VALUE = "None"

    def __init__(self):
        self.user_input: UserInput = UserInput(self.DEFAULT_USER_INPUT_VALUE)
