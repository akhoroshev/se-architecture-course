from abc import ABC, abstractmethod
from typing import Iterable


class IToken(ABC):
    """
    Base class for Token
    """
    @abstractmethod
    def is_delimiter(self) -> bool:
        pass

    @abstractmethod
    def is_pipe(self) -> bool:
        pass

    @abstractmethod
    def get_content(self) -> str:
        pass


class TokenString(IToken):
    """
    Token that can contain string
    """
    def is_pipe(self) -> bool:
        return self.content == "|"

    def __init__(self, content):
        self.content = content

    def is_delimiter(self) -> bool:
        return False

    def get_content(self) -> str:
        return self.content

    def __repr__(self):
        return f"TokenString: {self.content}"

    def __eq__(self, other):
        return isinstance(other, TokenString) and other.content == self.content

    @staticmethod
    def join(iterable: Iterable[IToken]) -> IToken:
        """
        Concat tokens
        """
        content = str()
        for i in iterable:
            content = content + i.get_content() if not i.is_delimiter() else content
        return TokenString(content)


class TokenDelimiter(IToken):
    """
    Token for represent delimiter
    """
    def is_pipe(self) -> bool:
        return False

    def is_delimiter(self) -> bool:
        return True

    def get_content(self):
        return None

    def __repr__(self):
        return "TokenDelimiter"

    def __eq__(self, other):
        return isinstance(other, TokenDelimiter)

    @staticmethod
    def join(iterable: Iterable[IToken]) -> Iterable[IToken]:
        """
        Insert delimiter between all tokens
        """
        iterator = iter(iterable)
        try:
            yield next(iterator)
        except StopIteration:
            return
        for item in iterator:
            yield TokenDelimiter()
            yield item
