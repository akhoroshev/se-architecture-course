from unittest import TestCase

from src.command import ICommand
from src.parser import create_parser, ParserCommandNotFound
from src.token import TokenDelimiter as TokDel
from src.token import TokenString as TokStr


class TestIParser(TestCase):
    def setUp(self):
        class MockCommand(ICommand):
            def execute(self) -> None:
                pass

        self.parser = create_parser()
        self.parser.add_command(MockCommand, 'run', False)
        self.parser.add_command(MockCommand, '=', True)

    def test_empty_command(self):
        self.assertEqual(0, len(self.parser.parse([])))

    def test_find_one_command(self):
        self.assertEqual(1, len(self.parser.parse([TokStr('run')])))
        self.assertEqual(1, len(self.parser.parse([TokStr('a'), TokStr('='), TokStr('b')])))

    def test_find_many_commands(self):
        self.assertEqual(2, len(self.parser.parse([TokStr('run'), TokStr('|'), TokStr('a'), TokStr('='), TokStr('b')])))

    def test_prefix_arg_parse(self):
        cmds = self.parser.parse(
            [TokStr('run'), TokStr('a'), TokStr('='), TokStr('b'), TokStr('|'), TokStr('run'), TokStr('a'), TokDel(),
             TokStr('='), TokDel(), TokStr('c')])
        self.assertEqual(2, len(cmds))
        self.assertEqual(("a=b",), cmds[0].m_args)
        self.assertEqual(("a", "=", "c"), cmds[1].m_args)

    def test_infix_arg_parse(self):
        cmds = self.parser.parse(
            [TokStr('a'), TokStr('='), TokStr('b'), TokStr('c'), TokStr('|'), TokStr('a'), TokStr('='), TokStr('b'),
             TokDel(), TokStr('c')])
        self.assertEqual(2, len(cmds))
        self.assertEqual(("a", "bc"), cmds[0].m_args)
        self.assertEqual(("a", "b", "c"), cmds[1].m_args)

    def test_command_not_found(self):
        self.assertRaises(ParserCommandNotFound, self.parser.parse, [TokStr(' ')])
        self.assertRaises(ParserCommandNotFound, self.parser.parse, [TokStr('no_command')])
