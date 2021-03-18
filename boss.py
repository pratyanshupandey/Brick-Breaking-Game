from config import *
from time import time
from bomb import Bomb


class Boss:
    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = BOSS_Y
        self.strength = BOSS_HEALTH
        self.last_bomb = time()

    def move(self, paddle):
        self.x = paddle.x
        if self.x - BOSS_WIDTH // 2 <= 0:
            self.x = 1 + BOSS_WIDTH // 2
        if self.x + BOSS_WIDTH // 2 >= SCREEN_COLS - 1:
            self.x = SCREEN_COLS - 2 - BOSS_WIDTH // 2
        if time() - self.last_bomb >= BOSS_BOMB_TIMEOUT:
            self.last_bomb = time()
            return Bomb(self.x)
        return None
