from unittest import TestCase
from src.environment import create_environment
from src.preprocessor import create_preprocessor


class TestPreprocessor(TestCase):
    def setUp(self):
        self.environment = create_environment()
        self.environment.add("foo", "bar")
        self.environment.add("bar", "foo")
        self.preprocessor = create_preprocessor()

    def parse(self, string):
        return self.preprocessor.process(string, self.environment)

    def test_substitution(self):
        self.assertEqual(["foo"], self.parse("foo"))
        self.assertEqual(["bar"], self.parse("$foo"))
        self.assertEqual(["$foo"], self.parse("'$foo'"))
        self.assertEqual(["barfoo"], self.parse("$foo$bar"))
        self.assertEqual(["barbar"], self.parse("$foo$foo"))
        self.assertEqual(["$foo$foo"], self.parse("'$foo$foo'"))
        self.assertEqual(["bar", " ",  "foo"], self.parse("$foo $bar"))
        self.assertEqual(["cat", " ", "bar", " ", "foo"], self.parse("cat $foo      $bar"))
        self.assertEqual(["cat", " ", "$foo     $bar"], self.parse("cat '$foo     $bar'"))

    def test_whitespace(self):
        self.assertEqual(["    ", " ", "bar"], self.parse("'    ' $foo"))
        # self.assertEqual(["    ", "bar"], self.parse("'    '$foo"))

    def test_pipe_split(self):
        self.assertEqual(["|"], self.parse("|"))
        self.assertEqual(["cat", " ", "|", " ", "bar", "|", "foo"], self.parse("cat   |   $foo|$bar"))
        self.assertEqual(["cat", "|", "$foo|$foo"], self.parse("cat|'$foo|$foo'"))

    def test_eq(self):
        self.assertEqual(["a", "=", "b"], self.parse("a=b"))
        self.assertEqual(["a", "=", "b"], self.parse("a=b   "))
        self.assertEqual(["a", "=", "b"], self.parse("   a=b"))
        self.assertEqual(["a", " ", "=", " ", "b"], self.parse("a   = b"))
