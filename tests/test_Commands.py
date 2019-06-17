import os
from unittest import TestCase

from src.commands import Cat
from src.commands import Echo
from src.commands import BinaryOperator
from src.commands import Pwd
from src.commands import Signal
from src.commands import Wc
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
