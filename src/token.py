from abc import ABC, abstractmethod


class IToken(ABC):
    @abstractmethod
    def is_delimiter(self) -> bool:
        pass

    @abstractmethod
    def get_content(self) -> str:
        pass


class TokenString(IToken):
    def __init__(self, content):
        self.content = content

    def is_delimiter(self):
        return False

    def get_content(self):
        return self.content

    def __repr__(self):
        return f"TokenString: {self.content}"

    def __eq__(self, other):
        return isinstance(other, TokenString) and other.content == self.content


class TokenDelimiter(IToken):
    def is_delimiter(self):
        return True

    def get_content(self):
        return None

    def __repr__(self):
        return "TokenDelimiter"

    def __eq__(self, other):
        return isinstance(other, TokenDelimiter)

    @staticmethod
    def join(iterable):
        iterator = iter(iterable)
        try:
            yield next(iterator)
        except StopIteration:
            return
        for item in iterator:
            yield TokenDelimiter()
            yield item
