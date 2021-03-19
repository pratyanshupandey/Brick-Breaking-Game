from config import *
from time import time
from bomb import Bomb


class Boss:
    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = BOSS_Y
        self.strength = BOSS_HEALTH
        self.last_bomb = time()
        self.brick_left = 2

    def move(self, paddle):
        if self.x == paddle.x:
            self.x += 0
        elif self.x < paddle.x:
            self.x += BOSS_VEL
        elif self.x > paddle.x:
            self.x -= BOSS_VEL

        if round(self.x - BOSS_WIDTH // 2) <= 0:
            self.x = 1 + BOSS_WIDTH // 2
        if round(self.x + BOSS_WIDTH // 2) >= SCREEN_COLS - 1:
            self.x = SCREEN_COLS - 2 - BOSS_WIDTH // 2
        if time() - self.last_bomb >= BOSS_BOMB_TIMEOUT:
            self.last_bomb = time()
            return Bomb(self.x)
        return None

    def before_brick(self, ball, brick):
        if ball.y_velocity > 0:
            return True
        return False