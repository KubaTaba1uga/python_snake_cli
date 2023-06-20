import logging
import traceback

from src.constants import LOGS_DIR


def _create_file_handler(file_name):
    file_handler = logging.FileHandler(file_name, "w")
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def _create_display_handlers():
    FILE_PATH = LOGS_DIR.joinpath("display.log").absolute()

    file_handler = _create_file_handler(FILE_PATH)

    return [file_handler]


def _create_display_logger():
    logger = logging.getLogger("display")

    logger.setLevel(logging.DEBUG)

    for handler in _create_display_handlers():
        logger.addHandler(handler)

    return logger


def _create_controller_handlers():
    FILE_PATH = LOGS_DIR.joinpath("controller.log").absolute()

    file_handler = _create_file_handler(FILE_PATH)

    return [file_handler]


def _create_controller_logger():
    logger = logging.getLogger("controller")

    logger.setLevel(logging.DEBUG)

    for handler in _create_controller_handlers():
        logger.addHandler(handler)

    return logger


def _create_game_engine_handlers():
    FILE_PATH = LOGS_DIR.joinpath("game.log").absolute()

    file_handler = _create_file_handler(FILE_PATH)

    return [file_handler]


def _create_game_engine_logger():
    logger = logging.getLogger("game_engine")

    logger.setLevel(logging.DEBUG)

    for handler in _create_game_engine_handlers():
        logger.addHandler(handler)

    return logger


_display_logger = _create_display_logger()
_controller_logger = _create_controller_logger()
_game_engine_logger = _create_game_engine_logger()


def get_display_logger():
    return _display_logger


def get_controller_logger():
    return _controller_logger


def get_game_engine_logger():
    return _game_engine_logger


def log_info(logger, msg):
    logger.info(msg)


def log_display_info(msg: str):
    logger = get_display_logger()

    log_info(logger, msg)


def log_controller_info(msg: str):
    logger = get_controller_logger()

    log_info(logger, msg)


def log_game_engine_info(msg: str):
    logger = get_game_engine_logger()

    log_info(logger, msg)


def log_error(function, logger):
    def wrapped_func(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            tb = traceback.format_exc()
            logger.error(tb)
            raise

    return wrapped_func


def log_display_error(function):
    logger = get_display_logger()

    return log_error(function, logger)


def log_controller_error(function):
    logger = get_controller_logger()

    return log_error(function, logger)


def log_game_engine_error(function):
    logger = get_game_engine_logger()

    return log_error(function, logger)
