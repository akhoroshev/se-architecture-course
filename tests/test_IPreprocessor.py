from unittest import TestCase
from src.environment import create_environment
from src.preprocessor import create_preprocessor
from src.token import TokenDelimiter as TokDel
from src.token import TokenString as TokStr


class TestPreprocessor(TestCase):
    def setUp(self):
        self.environment = create_environment()
        self.environment.add("foo", "bar")
        self.environment.add("bar", "foo")
        self.environment.add("echofoo", "echo foo")
        self.environment.add("echopipe", "echo pipe | cat")
        self.environment.add("a", "1")
        self.preprocessor = create_preprocessor()
        self.preprocessor.set_environment(self.environment)

    def parse(self, string):
        return self.preprocessor.process(string)

    def test_substitution(self):
        self.assertEqual([TokStr("foo")], self.parse("foo"))
        self.assertEqual([TokStr("bar")], self.parse("$foo"))
        self.assertEqual([TokStr("$foo")], self.parse("'$foo'"))
        self.assertEqual([TokStr("barfoo")], self.parse("$foo$bar"))
        self.assertEqual([TokStr("barbar")], self.parse("$foo$foo"))
        self.assertEqual([TokStr("$foo$foo")], self.parse("'$foo$foo'"))
        self.assertEqual([TokStr("bar"), TokDel(), TokStr("foo")], self.parse("$foo $bar"))
        self.assertEqual(
            [TokStr("cat"), TokDel(), TokStr("bar"), TokDel(), TokStr("foo")],
            self.parse("cat $foo      $bar"))
        self.assertEqual([TokStr("cat"), TokDel(), TokStr("$foo     $bar")],
                         self.parse("cat '$foo     $bar'"))
        self.assertEqual([TokStr("echo"), TokDel(), TokStr("foo")], self.parse("$echofoo"))
        self.assertEqual([TokStr("echo foo")], self.parse('"$echofoo"'))

    def test_whitespace(self):
        self.assertEqual([TokStr("    "), TokDel(), TokStr("bar")], self.parse("'    ' $foo"))
        self.assertEqual([TokStr("    bar")], self.parse("'    '$foo"))
        self.assertEqual([], self.parse("      "))
        self.assertEqual([TokStr('      ')], self.parse("'      '"))

    def test_pipe_split(self):
        self.assertEqual([TokStr("|")], self.parse(" |   "))
        self.assertEqual([TokStr("|"), TokStr("|"), TokDel(), TokStr("|")], self.parse("|| |  "))

        self.assertEqual([TokStr("cat"), TokDel(), TokStr("|"),
                          TokDel(), TokStr("bar"), TokStr("|"),
                          TokStr("foo")], self.parse("cat   |   $foo|$bar"))
        self.assertEqual([TokStr("cat"), TokStr("|"), TokStr("$foo|$foo")],
                         self.parse("cat|'$foo|$foo'"))
        self.assertEqual([TokStr("echo"), TokDel(), TokStr("pipe"), TokDel(),
                          TokStr("|"), TokDel(), TokStr("cat")], self.parse("$echopipe"))

    def test_eq(self):
        self.assertEqual([TokStr("a"), TokStr("="), TokStr("b")], self.parse("  a=b "))
        self.assertEqual([TokStr("a"), TokDel(), TokStr("="), TokDel(), TokStr("b")],
                         self.parse("  a   = b  "))

    def test_whitespace_in_quotes(self):
        self.assertEqual([TokStr("echo"), TokDel(), TokStr("asdasd1")], self.parse('echo "asdasd$a"'))
        self.assertEqual([TokStr("echo"), TokDel(), TokStr("asdasd 1")],
                         self.parse('echo "asdasd $a"'))
        self.assertEqual([TokStr("echo"), TokDel(), TokStr("asdasd1")], self.parse('echo asdasd$a'))
        self.assertEqual(
            [TokStr("echo"), TokDel(), TokStr("asdasd"), TokDel(), TokStr("1")],
            self.parse('echo asdasd $a'))
