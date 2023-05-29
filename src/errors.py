class UnableToRecognizeKey(BaseException):
    def __init__(self, key=None):
        if key is not None:
            self.key = key

        super().__init__(key)


class PleaseUseContextManagerError(BaseException):
    """Thread based objects should be used as context manager, so user
    do not need to bother about implementation details. Please do not
    catch this error."""

    def __init__(self, function, cls=None, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.cls = cls

        super().__init__(function, args, kwargs)
