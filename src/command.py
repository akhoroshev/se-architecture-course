from abc import ABC, abstractmethod
from os import getcwd

from src.stream import IStream


class CommandArgumentCountError(ValueError):
    def __init__(self, string):
        super().__init__(f"{string}: argument count error")


class ICommand(ABC):
    """
    Abstract class for command
    Each command has name, args, input/output stream
    """
    def __init__(self, name: str, *args: str):
        self.m_name = name
        self.m_args = args
        self.m_inp_stream = None
        self.m_out_stream = None

    @abstractmethod
    def execute(self) -> None:
        """
        Function will be called when command execution is required
        """
        pass

    def set_input_stream(self, stream: IStream) -> None:
        """
        Setter for input stream
        """
        self.m_inp_stream = stream

    def get_input_stream(self) -> IStream:
        """
        Getter for input stream
        """
        return self.m_inp_stream

    def set_output_stream(self, stream: IStream) -> None:
        """
        Setter for output stream
        """
        self.m_out_stream = stream

    def get_output_stream(self) -> IStream:
        """
        Getter for output stream
        """
        return self.m_out_stream


class IFsCommand(ICommand):
    """
    Base class for command interacting with the file system
    """

    m_current_dir = None

    def __init__(self, name, *args):
        super().__init__(name, *args)
        if not IFsCommand.m_current_dir:
            IFsCommand.m_current_dir = getcwd()

    @abstractmethod
    def execute(self) -> None:
        """
        Function will be called when command execution is required
        """
        pass
