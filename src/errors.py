class UnableToRecognizeKey(Exception):
    def __init__(self, key=None):
        if key is not None:
            self.key = key

        super().__init__(key)


class PleaseUseContextManagerError(Exception):
    """Thread based objects should be used as context manager, so user
    do not need to bother about implementation details. Please do not
    catch this error."""

    def __init__(self, function, cls=None, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.cls = cls

        super().__init__(function, args, kwargs)


class NoSelectedField(Exception):
    def __init__(self, fields_map, ctx):
        self.fields_map = fields_map
        self.ctx = ctx

        super().__init__(fields_map, ctx)

    def __str__(self):
        return f"{self.ctx} \n {self.fields_map}"


class ValidationError(Exception):
    """Invalid value."""

    def __str__(self):
        return "VALIDATION ERROR"


class SnakeDied(Exception):
    """Snake is dead ."""

    def __init__(self, snake):
        self.snake = snake

        super().__init__(snake)

    def __str__(self):
        return f"SNAKE IS DEAD ERROR {str(self.snake)}"
