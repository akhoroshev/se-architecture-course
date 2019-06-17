import re
from argparse import ArgumentParser

from src.command import IFsCommand


class GrepArgParseError(ValueError):
    def __init__(self, string):
        super().__init__(string)


class GrepExit(ValueError):
    pass


class GrepArgParser(ArgumentParser):
    """
    Class with modified behaviour on error and exit.
    Original error and exit methods in ArgumentParser stop the application with exit code.
    """
    def error(self, message):
        raise GrepArgParseError(message)

    def exit(self, *_):
        raise GrepExit()


class Grep(IFsCommand):
    """
    Grep command.
    Command line argument parsing implemented with python argparse library because
    Argparse makes life easy by providing us a way to define the commonly used validations for command line arguments.
    """
    def __init__(self, name, *args):
        super().__init__(name, *args)
        self.parser = GrepArgParser('Search for PATTERN in each FILE or standard input.')
        self.parser.add_argument('PATTERN', nargs=1)
        self.parser.add_argument('FILE', nargs='*', )
        self.parser.add_argument('-i', '--ignore-case', help='ignore case distinctions',
                                 action='store_true', default=False)
        self.parser.add_argument('-w', '--word-regexp', help='force PATTERN to match only whole words',
                                 action='store_true', default=False)
        self.parser.add_argument('-A', help='print NUM lines of trailing context',
                                 type=int, action='store', default=0)

    def execute(self) -> None:
        try:
            parsed_args = self.parser.parse_args(list(self.m_args))
            if parsed_args.A < 0:
                raise GrepArgParseError(f'{self.m_name}: -1: invalid context length argument')
            if parsed_args.FILE:
                for file in parsed_args.FILE:
                    print(self.handle_input(parsed_args, file), file=self.m_out_stream, flush=True, end='')
            else:
                print(self.handle_input(parsed_args), file=self.m_out_stream, flush=True, end='')
        except GrepExit:
            pass

    def handle_input(self, parsed_args, input_name=None):
        if not input_name:
            return self.__grep(parsed_args, self.m_inp_stream)
        with open(input_name, "r") as file:
            return self.__grep(parsed_args, file)

    @staticmethod
    def __grep(parsed_args, handle):
        re_flags = re.IGNORECASE if parsed_args.ignore_case else 0
        re_pattern = " {} ".format(parsed_args.PATTERN[0]) if parsed_args.word_regexp else parsed_args.PATTERN[0]
        result = list()
        skip = 0
        for line in handle:
            if skip > 0:
                result.append(line)
                skip -= 1
                continue
            if re.search(re_pattern, line, flags=re_flags):
                result.append(line)
                skip = parsed_args.A
        return ''.join(result)
