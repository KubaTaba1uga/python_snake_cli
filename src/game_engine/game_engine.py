import typing

from src.user_input import UserInput


class GameEngine:
    def __init__(self):
        self.user_input: UserInput = UserInput("None")
