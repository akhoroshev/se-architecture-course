from abc import ABC, abstractmethod
from src.environment import IEnvironment
import shlex


class PreprocessorParseError(ValueError):
    def __init__(self, string):
        super().__init__(f"{string}: parse error")


class IPreprocessor(ABC):
    @abstractmethod
    def process(self, string: str, environment: IEnvironment) -> [str]:
        """
        Function split input string and make substitutions if needed
        :param string: str
        :param environment: IEnvironment
        """
        pass


def create_preprocessor() -> IPreprocessor:
    return PreprocessorImpl()


##################
# Implementation #
##################

class PreprocessorImpl(IPreprocessor):
    def process(self, string: str, environment: IEnvironment) -> [str]:
        try:
            whitespace_split = split_whitespace(string)
            # print(f"whitespace_split: {whitespace_split}")
            whitespace_splitted = [split_symbols(i) for i in whitespace_split]
            # print(f"whitespace_splitted: {whitespace_splitted}")
            whitespace_separated = merge_list(whitespace_splitted, " ")
            # print(f"whitespace_separated: {whitespace_separated}")
            return [PreprocessorImpl.lex_token(token, environment) for token in whitespace_separated]
        except ValueError:
            raise PreprocessorParseError(string)

    @staticmethod
    def lex_token(string: str, environment: IEnvironment) -> str:
        if string == " ":
            return " "
        result_token = str()
        tokens = list(shlex.shlex(string))
        tokens = [unquote(tok) for tok in tokens]
        need_ref = False
        for token in tokens:
            if need_ref:
                result_token += environment.get(token)
            elif token != '$':
                result_token += token
            if token == '$':
                need_ref = True
            else:
                need_ref = False
        if need_ref:
            raise PreprocessorParseError(string)
        return result_token


def split_whitespace(string: str) -> [str]:
    lex = shlex.shlex(string)
    lex.whitespace_split = True
    return list(lex)


def split_symbols(string: str) -> [str]:
    lex = shlex.shlex(string)
    lex.wordchars += '$'
    return list(lex)


def unquote(string: str):
    if string.startswith('"') or string.startswith("'"):
        string = string[1:]

    if string.endswith('"') or string.endswith("'"):
        string = string[:-1]
    return string


def merge_list(lists, delimiter):
    [i.append(delimiter) for i in lists[:-1]]
    merged_list = list()
    [merged_list.extend(i) for i in lists]
    return merged_list
