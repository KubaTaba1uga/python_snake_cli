import logging


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
