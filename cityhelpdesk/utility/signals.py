# coding=utf-8
"""
Utilities for signals
"""


class SignalSpy(object):
    """Signal spy that is used to check if signals are received."""

    def __init__(self):
        self.count = 0

    def receiver(self, **kwargs):
        self.count += 1

    def received_count(self):
        return self.count

    def received_signal(self):
        return self.count > 0

    def reset(self):
        self.count = 0


class KwargsSignalSpy(SignalSpy):

    def __init__(self):
        super(KwargsSignalSpy, self).__init__()
        self.kwargs = {}

    def receiver(self, **kwargs):
        super(KwargsSignalSpy, self).receiver()
        self.kwargs = kwargs
