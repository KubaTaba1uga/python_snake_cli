class COLORS_FOREGROUND:
    RED = "\033[31m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    WHITE = "\033[37m"
    BLUE = "\033[34m"
    BLACK = "\033[30m"


class COLORS_BACKGROUND:
    RED = "\033[41m"
    WHITE = "\033[47m"
    BLUE = "\033[44m"
    BLACK = "\033[40m"


class ESCAPE:
    START_AGAIN = "\033[1K"
    ENDC = "\033[0m"


def paint_red(string: str, is_background: bool = False) -> str:
    return (
        f"{COLORS_BACKGROUND.RED if is_background else COLORS_FOREGROUND.RED}"
        f"{string}{ESCAPE.ENDC}"
    )


def paint_white(string: str, is_background: bool = False) -> str:
    return (
        f"{COLORS_BACKGROUND.WHITE if is_background else COLORS_FOREGROUND.WHITE}"
        f"{string}{ESCAPE.ENDC}"
    )


def paint_blue(string: str, is_background: bool = False) -> str:
    return (
        f"{COLORS_BACKGROUND.BLUE if is_background else COLORS_FOREGROUND.BLUE}"
        f"{string}{ESCAPE.ENDC}"
    )


def paint_black(string: str, is_background: bool = False) -> str:
    return (
        f"{COLORS_BACKGROUND.BLACK if is_background else COLORS_FOREGROUND.BLACK}"
        f"{string}{ESCAPE.ENDC}"
    )


def paint_bold(string: str) -> str:
    return f"{COLORS_FOREGROUND.BOLD}{string}{ESCAPE.ENDC}"


def move_cursor_to_line_beginning(string: str) -> str:
    return f"{ESCAPE.START_AGAIN}{string}{ESCAPE.ENDC}"
