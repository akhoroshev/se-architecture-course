from abc import ABC, abstractmethod
from src.command import ICommand


class ParserParseError(ValueError):
    def __init__(self, string):
        super().__init__(f"{string}: parse error")


class ParserCommandNotFound(LookupError):
    def __init__(self, string):
        super().__init__(f"{string}: command not found")


class IParser(ABC):
    @abstractmethod
    def parse(self, tokens: [str]) -> [ICommand]:
        """
        Constructs an array of commands from an array of tokens
        :param tokens: [str]
        """
        pass

    @abstractmethod
    def add_command(self, command_constructor, name: str, infix: bool):
        """
        Associate a token with a command.
        Command can be prefix or infix
        :param command_constructor: callable
        :param name: str
        :param infix: bool
        """
        pass

    @abstractmethod
    def set_default_command(self, command_constructor):
        """
        Default command if token unknown
        :param command_constructor: callable
        """
        pass


def create_parser() -> IParser:
    return ParserImpl()


##################
# Implementation #
##################

class ParserImpl(IParser):
    def __init__(self):
        self.m_prefix_command_map = dict()
        self.m_infix_command_map = dict()
        self.m_default_command = None

    def add_command(self, command_constructor, name: str, infix: bool):
        if infix:
            self.m_infix_command_map[name] = command_constructor
        else:
            self.m_prefix_command_map[name] = command_constructor

    def set_default_command(self, command_constructor):
        self.m_default_command = command_constructor

    def parse(self, tokens: [str]) -> [ICommand]:
        if not tokens:
            return list()

        command_tokens = split_list(tokens, "|")
        command_tokens = [eat_prefix_whitespaces(i) for i in command_tokens]

        if not check_not_empty_commands(command_tokens):
            raise ParserParseError(''.join(tokens))

        return [self.parse_command_tokens(i) for i in command_tokens]

    def parse_command_tokens(self, tokens: [str]) -> ICommand:
        if tokens[0] in self.m_prefix_command_map:
            whitespace_split = split_list(tokens[1:], " ")
            args = [''.join(i) for i in filter(lambda x: len(x) > 0, whitespace_split)]
            return self.m_prefix_command_map[tokens[0]](tokens[0], *args)
        elif len(tokens) > 1 and tokens[1] in self.m_infix_command_map:
            whitespace_split = split_list(tokens[0:1] + [" "] + tokens[2:], " ")
            args = [''.join(i) for i in filter(lambda x: len(x) > 0, whitespace_split)]
            return self.m_infix_command_map[tokens[1]](tokens[1], *args)

        if self.m_default_command:
            whitespace_split = split_list(tokens[1:], " ")
            args = [''.join(i) for i in filter(lambda x: len(x) > 0, whitespace_split)]
            return self.m_default_command(tokens[0], *args)

        raise ParserCommandNotFound(tokens[0])


def eat_prefix_whitespaces(array: list) -> list:
    k = 0
    for i in array:
        if i == " ":
            k += 1
        else:
            break
    return array[k:]


def check_not_empty_commands(array: list) -> bool:
    for i in array:
        if len(i) == 0:
            return False
    return True


def split_list(array: list, delimiter) -> [list]:
    result = list()
    last_list = list()
    for i in array:
        if i == delimiter:
            result.append(last_list)
            last_list = list()
        else:
            last_list.append(i)
    result.append(last_list)
    return result
