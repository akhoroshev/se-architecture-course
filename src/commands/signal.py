from typing import Callable

from src.command import ICommand


class Signal(ICommand):
    """
    Wrapper for signal
    """
    def __init__(self, callback: Callable[[], None], name: str):
        super().__init__(name)
        self.callback = callback

    def execute(self) -> None:
        self.callback()
