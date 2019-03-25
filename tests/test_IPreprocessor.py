from unittest import TestCase
from src.environment import create_environment
from src.preprocessor import create_preprocessor
from src.token import TokenDelimiter, TokenString


class TestPreprocessor(TestCase):
    def setUp(self):
        self.environment = create_environment()
        self.environment.add("foo", "bar")
        self.environment.add("bar", "foo")
        self.environment.add("echofoo", "echo foo")
        self.environment.add("echopipe", "echo pipe | cat")
        self.preprocessor = create_preprocessor()
        self.preprocessor.set_environment(self.environment)

    def parse(self, string):
        return self.preprocessor.process(string)

    def test_substitution(self):
        self.assertEqual([TokenString("foo")], self.parse("foo"))
        self.assertEqual([TokenString("bar")], self.parse("$foo"))
        self.assertEqual([TokenString("$foo")], self.parse("'$foo'"))
        self.assertEqual([TokenString("barfoo")], self.parse("$foo$bar"))
        self.assertEqual([TokenString("barbar")], self.parse("$foo$foo"))
        self.assertEqual([TokenString("$foo$foo")], self.parse("'$foo$foo'"))
        self.assertEqual([TokenString("bar"), TokenDelimiter(), TokenString("foo")], self.parse("$foo $bar"))
        self.assertEqual([TokenString("cat"), TokenDelimiter(), TokenString("bar"), TokenDelimiter(), TokenString("foo")],
                         self.parse("cat $foo      $bar"))
        self.assertEqual([TokenString("cat"), TokenDelimiter(), TokenString("$foo     $bar")],
                         self.parse("cat '$foo     $bar'"))
        self.assertEqual([TokenString("echo"), TokenDelimiter(), TokenString("foo")], self.parse("$echofoo"))
        self.assertEqual([TokenString("echo foo")], self.parse('"$echofoo"'))

    def test_whitespace(self):
        self.assertEqual([TokenString("    "), TokenDelimiter(), TokenString("bar")], self.parse("'    ' $foo"))
        self.assertEqual([TokenString("    bar")], self.parse("'    '$foo"))

    def test_pipe_split(self):
        self.assertEqual([TokenString("|")], self.parse(" |   "))
        self.assertEqual([TokenString("|"), TokenString("|"), TokenDelimiter(), TokenString("|")], self.parse("|| |  "))

        self.assertEqual([TokenString("cat"), TokenDelimiter(), TokenString("|"),
                          TokenDelimiter(), TokenString("bar"), TokenString("|"),
                          TokenString("foo")], self.parse("cat   |   $foo|$bar"))
        self.assertEqual([TokenString("cat"), TokenString("|"), TokenString("$foo|$foo")], self.parse("cat|'$foo|$foo'"))
        self.assertEqual([TokenString("echo"), TokenDelimiter(), TokenString("pipe"), TokenDelimiter(),
                          TokenString("|"), TokenDelimiter(), TokenString("cat")], self.parse("$echopipe"))

    def test_eq(self):
        self.assertEqual([TokenString("a"), TokenString("="), TokenString("b")], self.parse("  a=b "))
        self.assertEqual([TokenString("a"), TokenDelimiter(), TokenString("="), TokenDelimiter(), TokenString("b")],
                         self.parse("  a   = b  "))
