from dataclasses import dataclass


@dataclass
class UserInput:
    _value: str

    def set(self, value: str):
        self._value = value

    def get(self) -> str:
        return self._value
