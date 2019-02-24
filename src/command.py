from abc import ABC, abstractmethod
from src.stream import IStream
from os import getcwd


class CommandArgumentCountError(ValueError):
    def __init__(self, string):
        super().__init__(f"{string}: argument count error")


class ICommand(ABC):
    def __init__(self, name, *args):
        """
        Base class for command
        :param name: str
        :param args: tuple
        """
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
        :param stream: IStream
        """
        self.m_inp_stream = stream

    def get_input_stream(self) -> IStream:
        """
        Getter for input stream
        :return: IStream
        """
        return self.m_inp_stream

    def set_output_stream(self, stream: IStream) -> None:
        """
        Setter for output stream
        :param stream: IStream
        """
        self.m_out_stream = stream

    def get_output_stream(self) -> IStream:
        """
        Getter for output stream
        :return: IStream
        """
        return self.m_out_stream


class IFsCommand(ICommand):
    m_current_dir = None

    def __init__(self, name, *args):
        """
        Base class for command interacting with the file system
        :param name: str
        :param args: tuple
        """
        super().__init__(name, *args)
        if not IFsCommand.m_current_dir:
            IFsCommand.m_current_dir = getcwd()

    @abstractmethod
    def execute(self) -> None:
        """
        Function will be called when command execution is required
        """
        pass
