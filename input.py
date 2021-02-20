"""Defining input class."""
import sys
import termios
import tty
import signal
from config import TIMEOUT
from time import time


class Get:
    """Class to get input."""

    def __call__(self):
        """Defining __call__."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        old_settings[3] = old_settings[3] & ~termios.ECHO
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class AlarmException(Exception):
    """Handling alarm exception."""
    pass


def alarmHandler(signum, frame):
    """Handling timeouts."""
    raise AlarmException


def input_to(getch, timeout=0.1):
    """Taking input from user."""
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getch()
        signal.alarm(0)
        return text
    except AlarmException:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        return None


def get_input():
    inputs = []
    begin = time()
    time_remaining = TIMEOUT - (time() - begin)
    while time_remaining > 0:
        inp = input_to(Get().__call__, time_remaining)
        if inp is not None:
            inputs.append(inp)
        time_remaining = TIMEOUT - (time() - begin)
    return inputs
