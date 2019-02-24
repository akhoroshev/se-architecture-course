from unittest import TestCase
from src.command import ICommand
from src.parser import create_parser, ParserCommandNotFound, ParserParseError


class TestIParser(TestCase):
    def setUp(self):
        class CheckArgsCommand(ICommand):
            def execute(self) -> None:
                pass

            def get_args(self):
                return self.m_args

        self.parser = create_parser()
        self.parser.add_command(CheckArgsCommand, 'run', False)
        self.parser.add_command(CheckArgsCommand, '=', True)

    def test_empty_command(self):
        self.assertEqual(0, len(self.parser.parse([])))

    def test_find_one_command(self):
        self.assertEqual(1, len(self.parser.parse(["run"])))
        self.assertEqual(1, len(self.parser.parse(["a", "=", "b"])))

    def test_find_many_commands(self):
        self.assertEqual(2, len(self.parser.parse(["run", "|", "a", "=", "b"])))
        self.assertEqual(3, len(self.parser.parse(["run", "a", "|", " ", "a", "=", "b", "|", " ", "run", "a", "b"])))

    def test_prefix_arg_parse(self):
        cmds = self.parser.parse(["run", "a", "=", "b", "|", "run", "a", " ", "=", " ", "c"])
        self.assertEqual(2, len(cmds))
        self.assertEqual(("a=b", ), cmds[0].get_args())
        self.assertEqual(("a", "=", "c"), cmds[1].get_args())

    def test_infix_arg_parse(self):
        cmds = self.parser.parse(["a", "=", "b", "c", " ", "|", "a", "=", " ", "b", " ", "c"])
        self.assertEqual(2, len(cmds))
        self.assertEqual(("a", "bc"), cmds[0].get_args())
        self.assertEqual(("a", "b", "c"), cmds[1].get_args())

    def test_empty_command_not_found(self):
        # self.assertRaises(ParserCommandNotFound, self.parser.parse, [" "])
        self.assertRaises(ParserCommandNotFound, self.parser.parse, ["      "])

    def test_command_not_found(self):
        self.assertRaises(ParserCommandNotFound, self.parser.parse, ["no_command"])

    def test_pipe_syntax_error(self):
        self.assertRaises(ParserParseError, self.parser.parse, ["|"])
        self.assertRaises(ParserParseError, self.parser.parse, ["|", "run"])
        self.assertRaises(ParserParseError, self.parser.parse, ["run", "|"])
        self.assertRaises(ParserParseError, self.parser.parse, ["|", "run", "|"])
