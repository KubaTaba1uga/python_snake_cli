class COLORS_FOREGROUND:
    RED = "\033[31m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class COLORS_BACKGROUND:
    RED = "\033[41m"


class ESCAPE:
    START_AGAIN = "\033[1K"
    ENDC = "\033[0m"


def paint_red(string: str, is_background: bool = False) -> str:
    return (
        f"{COLORS_BACKGROUND.RED if is_background else COLORS_FOREGROUND.RED}"
        f"{string}{ESCAPE.ENDC}"
    )


def paint_bold(string: str) -> str:
    return f"{COLORS_FOREGROUND.BOLD}{string}{ESCAPE.ENDC}"


def move_cursor_to_line_beginning(string: str) -> str:
    return f"{ESCAPE.START_AGAIN}{string}{ESCAPE.ENDC}"
