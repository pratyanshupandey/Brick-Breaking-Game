from config import *

class Paddle:
    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = SCREEN_ROWS - 3
        self.length = PAD_LEN
        self.is_sticky = False
    def move(self, inp):
        if inp == "a" and ((self.x - self.length//2) > 1):
            self.x -= PAD_VEL
        elif inp == "d" and ((self.x + self.length//2) < SCREEN_COLS - 2):
            self.x += PAD_VEL


