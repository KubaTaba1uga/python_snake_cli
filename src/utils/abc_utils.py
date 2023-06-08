from abc import ABC
from abc import abstractmethod


class ContextManagerAbs(ABC):
    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, exc_tryceback):
        pass


class NonBlockingAbs(ABC):
    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass
