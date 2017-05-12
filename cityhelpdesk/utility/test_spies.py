import unittest

from .signals import SignalSpy
from .signals import KwargsSignalSpy


class SignalSpyTest(unittest.TestCase):

    def test_spy_receive(self):
        # Create a spy
        spy = SignalSpy()

        # Trigger receiver
        spy.receiver()

        # Test received
        self.assertTrue(spy.received_signal())
        # Test received count
        self.assertEqual(spy.received_count(), 1)

        # Trigger receiver again
        spy.receiver()

        # Test received
        self.assertTrue(spy.received_signal())
        # Test received count
        self.assertEqual(spy.received_count(), 2)


    def test_reset(self):
        # Create spy
        spy = SignalSpy()

        # Trigger receiver
        spy.receiver()

        # Reset
        spy.reset()

        # Test received
        self.assertFalse(spy.received_signal())
        self.assertEqual(spy.received_count(), 0)


class KwargsSignalSpyTest(unittest.TestCase):

    def test_kwargs_spy_create(self):
        # Create a spy
        spy = KwargsSignalSpy()
        # Test count was properly initialized
        self.assertEqual(spy.received_count(), 0)

    def test_kwargs_spy_receive(self):
        # Create a spy
        spy = KwargsSignalSpy()
        # Trigger the receiver with kwargs
        kwargs = {
            "a": "apple",
            "b": "boy",
            "c": "chrysanthemum"
        }
        spy.receiver(**kwargs)
        self.assertEqual(spy.kwargs, kwargs)
