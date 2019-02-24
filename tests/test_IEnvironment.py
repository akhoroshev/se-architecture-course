from unittest import TestCase
from src.environment import create_environment, VariableNotFoundError


class TestIEnvironment(TestCase):
    def test_contains(self):
        env = create_environment()
        self.assertFalse(env.contains("foo"))
        env.add("foo", "bar")
        self.assertTrue(env.contains("foo"))

    def test_remove(self):
        env = create_environment()
        self.assertFalse(env.remove("foo"))
        env.add("foo", "bar")
        self.assertTrue(env.remove("foo"))

    def test_get(self):
        env = create_environment()
        self.assertRaises(VariableNotFoundError, env.get, "foo")
        env.add("foo", "bar")
        self.assertEqual(env.get("foo"), "bar")
