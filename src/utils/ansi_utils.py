class COLORS_FOREGROUND:
    RED = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


class COLORS_BACKGROUND:
    RED = "\033[41m"


def paint_red(string: str, is_background: bool = False) -> str:

    return f"{COLORS_BACKGROUND.RED if is_background else COLORS_FOREGROUND.RED}{string}{COLORS_FOREGROUND.ENDC}"
