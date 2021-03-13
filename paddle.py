from config import *


class Paddle:
    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = SCREEN_ROWS - PAD_VER_OFF
        self.length = PAD_LEN
        self.is_sticky = False
        self.is_shooter = False

    def move(self, inp):
        if inp == "a":
            self.x -= PAD_VEL
            if self.x - self.length // 2 <= 0:
                self.x = 1 + self.length // 2
        elif inp == "d":
            self.x += PAD_VEL
            if self.x + self.length // 2 >= SCREEN_COLS - 1:
                self.x = SCREEN_COLS - 2 - self.length // 2
