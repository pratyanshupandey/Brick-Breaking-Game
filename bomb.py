from config import *


class Bomb:
    def __init__(self, x):
        self.x = x
        self.y = BOMB_Y

    def move(self, paddle):
        ret_val = 0
        next_y = self.y + BOMB_VEL
        if next_y == paddle.y and (paddle.x - paddle.length // 2) <= self.x <= (paddle.x + paddle.length // 2):
            ret_val = 1

        self.y += BOMB_VEL

        if self.y >= SCREEN_ROWS - 1:
            ret_val = -1
        return ret_val
