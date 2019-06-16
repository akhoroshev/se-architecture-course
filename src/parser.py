from abc import ABC, abstractmethod
from typing import Callable, List, TypeVar, Any

from src.command import ICommand
from src.token import IToken, TokenDelimiter, TokenString


class ParserArgumentCountError(TypeError):
    def __init__(self, string):
        super().__init__(f"{string}: mismatched argument count")


class ParserCommandNotFound(LookupError):
    def __init__(self, string):
        super().__init__(f"{string}: command not found")


class IParser(ABC):
    """
    Interface for converting list of tokens to list of commands
    """
    @abstractmethod
    def parse(self, tokens: List[IToken]) -> List[ICommand]:
        """
        Constructs an array of commands from an array of tokens
        """
        pass

    @abstractmethod
    def add_command(self, command_factory: Callable[[str, Any], ICommand], name: str, infix: bool):
        """
        Associate a token with a command.
        Command can be prefix or infix
        """
        pass

    @abstractmethod
    def set_default_command(self, command_factory: Callable[[str, Any], ICommand]):
        """
        Default command if token unknown
        """
        pass


def create_parser() -> IParser:
    return ParserImpl()


##################
# Implementation #
##################


T = TypeVar('T')


class ParserImpl(IParser):
    def __init__(self):
        self.m_prefix_command_map = dict()
        self.m_infix_command_map = dict()
        self.m_default_command = None

    def parse(self, tokens: List[IToken]) -> List[ICommand]:
        command_seq = self.split_list_by_condition(tokens, lambda i: i.is_pipe())
        command_seq = map(self.remove_start_delimiters, command_seq)
        command_seq = filter(None, command_seq)
        return list(map(self.parse_command, command_seq))

    def parse_command(self, tokens: List[IToken]) -> ICommand:
        if tokens[0].get_content() in self.m_prefix_command_map:
            return ParserImpl.create_command(
                self.m_prefix_command_map[tokens[0].get_content()],
                tokens[0].get_content(),
                tokens[1:])
        elif len(tokens) > 1 and tokens[1].get_content() in self.m_infix_command_map:
            return ParserImpl.create_command(
                self.m_infix_command_map[tokens[1].get_content()],
                tokens[1].get_content(),
                [tokens[0], TokenDelimiter()] + tokens[2:])

        if self.m_default_command:
            return ParserImpl.create_command(
                self.m_default_command,
                tokens[0].get_content(),
                tokens[1:])

        raise ParserCommandNotFound(tokens[0].get_content())

    @staticmethod
    def create_command(command_factory: Callable[[str, Any], ICommand], name: str, args: List[IToken]) -> ICommand:
        args_seq = ParserImpl.split_list_by_condition(args, lambda i: i.is_delimiter())
        args_seq = filter(None, args_seq)
        args_seq = map(TokenString.join, args_seq)
        try:
            return command_factory(name, *list(map(lambda i: i.get_content(), args_seq)))
        except TypeError:
            raise ParserArgumentCountError(name)

    def add_command(self, command_factory: Callable[[str, Any], ICommand], name: str, infix: bool):
        if infix:
            self.m_infix_command_map[name] = command_factory
        else:
            self.m_prefix_command_map[name] = command_factory

    def set_default_command(self, command_factory: Callable[[str, Any], ICommand]):
        self.m_default_command = command_factory

    @staticmethod
    def remove_start_delimiters(seq: List[IToken]) -> List[IToken]:
        out = seq.copy()
        for o in out:
            if o.is_delimiter():
                out.remove(o)
            else:
                break
        return out

    @staticmethod
    def split_list_by_condition(seq: List[T], condition: Callable[[T], bool]) -> List[List[T]]:
        output = list()
        last_list = list()
        for o in seq:
            if condition(o):
                output.append(last_list)
                last_list = list()
            else:
                last_list.append(o)
        output.append(last_list)
        return output
