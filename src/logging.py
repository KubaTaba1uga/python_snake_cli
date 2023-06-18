import logging
import traceback


def _create_file_handler(file_name):
    file_handler = logging.FileHandler(file_name, "w")
    file_handler.setLevel(logging.DEBUG)
    return file_handler


def _create_snake_handlers():
    FILE_NAME = "snake.log"

    file_handler = _create_file_handler(FILE_NAME)

    return [file_handler]


def _create_snake_logger():
    logger = logging.getLogger("snake")

    logger.setLevel(logging.DEBUG)

    for handler in _create_snake_handlers():
        logger.addHandler(handler)

    return logger


_snake_logger = _create_snake_logger()


def get_snake_logger():
    return _snake_logger


def log_snake_info(msg: str):
    logger = get_snake_logger()

    logger.info(msg)


def log_snake_error(function):
    logger = get_snake_logger()

    def wrapped_func(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            tb = traceback.format_exc()
            logger.error(tb)

    return wrapped_func
