from abc import ABC, abstractmethod
from src.environment import IEnvironment
from src.token import IToken, TokenDelimiter, TokenString

from parsec import *
import shlex


class PreprocessorParseError(ValueError):
    def __init__(self, content):
        super().__init__(f"{content}: parse error")


class IPreprocessor(ABC):
    @abstractmethod
    def set_environment(self, environment: IEnvironment) -> None:
        pass

    @abstractmethod
    def get_environment(self) -> IEnvironment:
        pass

    @abstractmethod
    def process(self, content: str) -> [IToken]:
        """
        Function split input string and make substitutions if needed
        :param content:
        """
        pass


def create_preprocessor() -> IPreprocessor:
    return PreprocessorImpl()


##################
# Implementation #
##################

class PreprocessorImpl(IPreprocessor):
    def __init__(self):
        self.m_environment = None

    def set_environment(self, environment: IEnvironment) -> None:
        self.m_environment = environment

    def get_environment(self) -> IEnvironment:
        return self.m_environment

    def process(self, content: str) -> [IToken]:

        def pure(value):
            """
            pure :: a -> m a
            """
            return Parser(lambda _, index: Value.success(index, value))

        subst_comb = (string('$') >> many1(digit() | letter())).bind(lambda val: pure(self.make_subst(''.join(val))))
        double_quotes_comb = (string('"') >> many(subst_comb ^ none_of('"')) << string('"')). \
            parsecmap(''.join). \
            parsecmap(TokenString)
        single_quotes_comb = (string("'") >> many(none_of("'")) << string("'")). \
            parsecmap(''.join). \
            parsecmap(TokenString)
        space_eat_comb = spaces() >> pure(TokenDelimiter())
        any_char_comb = none_of(["'", '"', ' ']).parsecmap(TokenString)
        subst_tokens_comb = subst_comb. \
            parsecmap(shlex.split). \
            parsecmap(lambda lst: map(TokenString, lst)). \
            parsecmap(lambda lst: list(TokenDelimiter.join(lst)))

        content_prs_comb = many(double_quotes_comb |
                                single_quotes_comb |
                                subst_tokens_comb ^ any_char_comb |
                                space_eat_comb) < eof()

        parsed_tokens = content_prs_comb.parse(content)
        result = list()
        for item in parsed_tokens:
            if isinstance(item, list):
                result.extend(item)
            else:
                result.append(item)
        return self.collapse_tokens(result)

    def make_subst(self, value: str) -> str:
        if self.get_environment().contains(value):
            return self.get_environment().get(value)
        else:
            return str()

    def collapse_tokens(self, tokens):
        result = list()
        current = None
        for token in tokens:
            if token.is_delimiter() and current is not None:
                result.append(TokenString(current))
                result.append(TokenDelimiter())
                current = None
            elif token.is_delimiter() and len(result) and result[-1] != TokenDelimiter():
                result.append(TokenDelimiter())
            if not token.is_delimiter() and token.get_content() in "|=":
                if current is not None:
                    result.append(TokenString(current))
                    current = None
                result.append(TokenString(token.get_content()))
            elif not token.is_delimiter():
                current = token.get_content() if current is None else current + token.get_content()
        if current is not None:
            result.append(TokenString(current))
        if len(result) and result[-1] == TokenDelimiter():
            del result[-1]
        return result
