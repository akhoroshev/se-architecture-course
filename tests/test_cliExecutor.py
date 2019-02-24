from unittest import TestCase
from src.command import ICommand
from src.stream import create_string_stream
from src.cli_executor import CliExecutor


class TestCliExecutor(TestCase):
    def test_executing_change_stream(self):
        append_string = "foo"
        count_of_commands = 5

        class AppendToStream(ICommand):
            def execute(self) -> None:
                print(self.m_inp_stream.read() + append_string, end='', file=self.m_out_stream)

        commands = [AppendToStream('name') for _ in range(count_of_commands)]

        start_stream = create_string_stream()
        end_stream = create_string_stream()

        CliExecutor.execute_command_list(commands, start_stream, end_stream)
        end_stream.seek(0, 0)
        self.assertEqual(append_string * count_of_commands, end_stream.read())

    def test_executing_no_change_stream(self):
        class NoChangeStream(ICommand):
            def execute(self) -> None:
                print(self.m_inp_stream.read(), end='', file=self.m_out_stream)

        count_of_commands = 5
        commands = [NoChangeStream('name') for _ in range(count_of_commands)]

        input_string = "foo"
        start_stream = create_string_stream()
        start_stream.write(input_string)
        start_stream.seek(0, 0)
        end_stream = create_string_stream()

        CliExecutor.execute_command_list(commands, start_stream, end_stream)
        end_stream.seek(0, 0)
        self.assertEqual(input_string, end_stream.read())
