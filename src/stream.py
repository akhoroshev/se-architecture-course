from io import StringIO, TextIOWrapper
from sys import stdout, stdin

IStream = TextIOWrapper


def create_string_stream() -> IStream:
    return StringIO()


def get_stdin_stream() -> IStream:
    return stdin


def get_stdout_stream() -> IStream:
    return stdout
