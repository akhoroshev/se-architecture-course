import os
from unittest import TestCase

from src.commands import *
from src.command import ICommand
from src.stream import create_string_stream


class TestCommands(TestCase):
    @staticmethod
    def prepare_streams(cmd: ICommand, input_stream_content=None):
        start_stream = create_string_stream()
        end_stream = create_string_stream()
        cmd.set_input_stream(start_stream)
        cmd.set_output_stream(end_stream)
        if input_stream_content:
            start_stream.write(input_stream_content)
            start_stream.seek(0, 0)
        return start_stream, end_stream

    def test_cat(self):
        cmd = Cat("cat")
        i, o = self.prepare_streams(cmd, "hello world")
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("hello world", o.read())

    def test_echo(self):
        cmd = Echo("echo", "hello", "world")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("hello world\n", o.read())

    def test_signal(self):
        self.test_signal_state = None

        def set_state():
            self.test_signal_state = True

        cmd = Signal(set_state, "signal")
        cmd.execute()
        self.assertEqual(True, self.test_signal_state)

    def test_binary_operator(self):
        self.test_binary_operator_state = None

        def add(lhs: str, rhs: str):
            self.test_binary_operator_state = int(lhs) + int(rhs)

        cmd = BinaryOperator(add, "add", "1", "2")
        cmd.execute()
        self.assertEqual(3, self.test_binary_operator_state)

    def test_pwd(self):
        cmd = Pwd("pwd")
        i, o = self.prepare_streams(cmd)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual(os.getcwd() + '\n', o.read())

    def test_wc(self):
        cmd = Wc("wc")
        i, o = self.prepare_streams(cmd, "Test wc"
                                         "how lines"
                                         "there")
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual("       1       3      21\n", o.read())


class TestGrepCommand(TestCase):
    FILE = "FROM python:3.6-alpine\n" \
           "\n" \
           "COPY . '/app'\n" \
           "WORKDIR '/app'\n" \
           "\n" \
           "RUN pip install -r requirements.txt\n" \
           "\n" \
           "CMD ['python3', 'bash.py']\n"

    def test_negative_trailing_context(self):
        cmd = Grep("grep", "-A", "-1", "pip")
        i, o = TestCommands.prepare_streams(cmd, self.FILE)
        self.assertRaises(GrepArgParseError, cmd.execute)

    def test_normal_trailing_context(self):
        cmd = Grep("grep", "-A", "2", "pip")
        i, o = TestCommands.prepare_streams(cmd, self.FILE)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual('\n'.join(self.FILE.splitlines()[-3:]) + '\n', o.read())

    def test_ignore_case(self):
        cmd = Grep("grep", "-i", "from python")
        i, o = TestCommands.prepare_streams(cmd, self.FILE)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual(self.FILE.splitlines()[0] + '\n', o.read())

    def test_match_whole_words(self):
        cmd = Grep("grep", "-i", "requirements.txt")
        i, o = TestCommands.prepare_streams(cmd, self.FILE)
        cmd.execute()
        o.seek(0, 0)
        self.assertEqual(self.FILE.splitlines()[-3] + '\n', o.read())
