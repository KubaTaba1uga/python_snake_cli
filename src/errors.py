class UnableToRecognizeKey(ValueError):
    def __init__(self, key=None):
        if key is not None:
            self.key = key

        super().__init__(key)
