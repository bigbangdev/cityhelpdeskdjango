# coding=utf-8
"""
Tests for utility functions.
"""

from __future__ import unicode_literals
import os
import unittest

from .annoying import AllIps
from .annoying import get_env
from .annoying import get_int
from .annoying import get_str
from .annoying import get_bool
from .annoying import default_if_none, din

class AllIpTest (unittest.TestCase):
    """Tests for the ``AllIps`` class that's used to shim Django's ``DEBUG`` mode
    """

    def setUp (self):
        """Create an AllIps instance to start."""
        self.allips = AllIps()

    def test_ips (self):
        """Test to make sure that actual ip addresses are present."""
        self.assertTrue("0.0.0.0" in self.allips)
        self.assertTrue("127.0.0.1" in self.allips)

    def test_nonips (self):
        """These pass because ``AllIps`` is dumb."""
        self.assertTrue("hello" in self.allips)
        self.assertTrue("foo" in self.allips)


class OsEnvTest (unittest.TestCase):
    """Tests for the ``get_env``, ``get_int``, ``get_str``, and ``get_bool``
    functions."""

    def test_get_env (self):
        """Test fetching an item from the environment."""

        self.assertEqual(os.environ.get("PS1", ":"), get_env("PS1", ":"))
        self.assertEqual(os.environ.get("HOME", "/"), get_env("HOME", "/"))

    def test_get_int (self):
        """Test fetching an integer from the environment."""

        os.environ["TEST_GOOD_INT"] = "10"
        os.environ["TEST_BAD_INT_1"] = "A"
        os.environ["TEST_BAD_INT_2"] = "10.1"

        self.assertEqual(get_int("TEST_GOOD_INT"), 10)

        # No default means normalize to 0
        self.assertEqual(get_int("TEST_BAD_INT_1"), 0)

        # Put a default here
        self.assertEqual(get_int("TEST_BAD_INT_1", 10), 10)

        # Test integer processing
        self.assertEqual(get_int("TEST_BAD_INT_2"), 0)
        self.assertEqual(get_int("TEST_BAD_INT_3"), 0)

        # Clean up the envionment
        del os.environ["TEST_GOOD_INT"]
        del os.environ["TEST_BAD_INT_1"]
        del os.environ["TEST_BAD_INT_2"]

    def test_get_str (self):
        """Test fetching a string from the environment."""

        os.environ["TEST_GOOD_STRING"] = "world"
        self.assertEqual(get_str("TEST_GOOD_STRING"), u"world")
        del os.environ["TEST_GOOD_STRING"]

    def test_get_bool (self):
        """Test fetching a boolean from the environment."""

        os.environ["TEST_BOOL_TRUE_1"] = "1"
        self.assertTrue(get_bool("TEST_BOOL_TRUE_1"))
        del os.environ["TEST_BOOL_TRUE_1"]
        os.environ["TEST_BOOL_TRUE_2"] = "True"
        self.assertTrue(get_bool("TEST_BOOL_TRUE_2"))
        del os.environ["TEST_BOOL_TRUE_2"]
        os.environ["TEST_BOOL_TRUE_3"] = "true"
        self.assertTrue(get_bool("TEST_BOOL_TRUE_3"))
        del os.environ["TEST_BOOL_TRUE_3"]
        os.environ["TEST_BOOL_TRUE_4"] = "t"
        self.assertTrue(get_bool("TEST_BOOL_TRUE_4"))
        del os.environ["TEST_BOOL_TRUE_4"]

        os.environ["TEST_BOOL_FALSE_1"] = "0"
        self.assertFalse(get_bool("TEST_BOOL_FALSE_1"))
        del os.environ["TEST_BOOL_FALSE_1"]
        os.environ["TEST_BOOL_FALSE_2"] = "False"
        self.assertFalse(get_bool("TEST_BOOL_FALSE_2"))
        del os.environ["TEST_BOOL_FALSE_2"]
        os.environ["TEST_BOOL_FALSE_3"] = "false"
        self.assertFalse(get_bool("TEST_BOOL_FALSE_3"))
        del os.environ["TEST_BOOL_FALSE_3"]
        os.environ["TEST_BOOL_FALSE_4"] = "f"
        self.assertFalse(get_bool("TEST_BOOL_FALSE_4"))
        del os.environ["TEST_BOOL_FALSE_4"]
        os.environ["TEST_BOOL_FALSE_5"] = ""
        self.assertFalse(get_bool("TEST_BOOL_FALSE_5"))
        del os.environ["TEST_BOOL_FALSE_5"]

        self.assertFalse(get_bool("TEST_BOOL_FALSE_6"))

class HelperFunctionTests (unittest.TestCase):
    """
    Tests for various helper functions.
    """

    def test_default_if_none (self):
        """Test the default_if_none function."""
        self.assertEqual(default_if_none, din)
        self.assertEqual(din(None, 1), 1)
        self.assertEqual(din(None, None), None)
        self.assertEqual(din(1, 2), 1)