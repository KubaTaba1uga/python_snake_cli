from src.user_input import UserInput
from src.constants import GAME_ENGINE_CTX, GAME_MENU_CTX
from src.game_engine.game_menu import GameMenu


class GameEngine:
    DEFAULT_USER_INPUT_VALUE = "None"

    # Game has to start from menu to load first session
    DEFAULT_GAME_ENGINE_CTX = GAME_ENGINE_CTX.MENU

    def __init__(self):
        self.user_input: UserInput = UserInput(self.DEFAULT_USER_INPUT_VALUE)
        self.ctx: GAME_ENGINE_CTX = self.DEFAULT_GAME_ENGINE_CTX

        self._ENGINE_CTX_PROCESS_FUNC_MAP = {
            GAME_ENGINE_CTX.MENU: self._process_menu_ctx,
            GAME_ENGINE_CTX.GAME: self._process_engine_ctx,
        }

        self._session = None

    def _process_ctx(self):
        self._ENGINE_CTX_PROCESS_FUNC_MAP[self.ctx]()

    def _process_menu_ctx(self):
        game_menu = GameMenu(self._session)

        while game_menu.ctx != GAME_MENU_CTX.PLAY:
            game_menu.process_selected_field()

        self._load_session(game_menu.current_session)

        self.ctx = GAME_ENGINE_CTX.GAME

    def _load_session(self, session):
        # Initialize game logic based on a game session
        self._session = session

    def _process_engine_ctx(self):
        # 1. if no game session raise not implemented
        if self._session is None:
            raise NotImplementedError(self)
