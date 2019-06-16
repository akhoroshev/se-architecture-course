from typing import Callable

from src.command import ICommand


class BinaryOperator(ICommand):
    def __init__(self, callback: Callable[[str, str], None], name: str, lhs: str, rhs: str):
        super().__init__(name)
        self.callback = callback
        self.lhs = lhs
        self.rhs = rhs

    def execute(self) -> None:
        self.callback(self.lhs, self.rhs)
