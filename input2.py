import atexit
import sys
import termios


class KBHit:
    """
    Class to handle keyboard input
    A modified version of "https://stackoverflow.com/a/22085679"
    """

    def init(self):
        """
        Creates a KBHit object that you can call to do various keyboard things.
        """
        # Save the terminal settings
        self.fd = sys.stdin.fileno()
        self.new_term = termios.tcgetattr(self.fd)
        self.old_term = termios.tcgetattr(self.fd)

        # New terminal setting unbuffered
        self.new_term[3] = (self.new_term[3] & ~
                              termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """
        Resets to normal terminal
        """
        termios.tcsetattr(self.fd, termios.TCSAFLUSH, self.__old_term)

    @staticmethod
    def getch():
        """
        Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        """
        return sys.stdin.read(1)

    @staticmethod
    def kbhit():
        """
        Returns True if keyboard character was hit, False otherwise.
        """
        return select([sys.stdin], [], [], 0)[0] != []

    @staticmethod
    def clear():
        """
        Clears the input buffer
        """
        termios.tcflush(sys.stdin, termios.TCIFLUSH)

kbhit = KBHit()
