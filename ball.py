from config import *
import random


class Ball:

    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = SCREEN_ROWS - 4
        self.is_stuck = True
        self.offset = 0
        # self.offset = random.randint(-1 * (PAD_LEN // 2), PAD_LEN // 2)
        self.x_velocity = self.offset
        self.y_velocity = -1
        self.strength = 1

    def move(self, paddle):
        ret_val = True
        if self.is_stuck:
            self.x = paddle.x + self.offset

        else:
            next_x = self.x + self.x_velocity
            next_y = self.y + self.y_velocity

            if next_x <= 0 or next_x >= SCREEN_COLS - 1:
                self.v_reflection()

            if next_y <= UPPER_WALL:
                self.h_reflection()

            if next_y >= SCREEN_ROWS - 1:
                ret_val = False

            if next_y == paddle.y and (paddle.x - paddle.length // 2) <= next_x <= (paddle.x + paddle.length // 2):
                self.y_velocity = -1 * self.y_velocity
                self.x_velocity += next_x - paddle.x

            self.x += self.x_velocity
            self.y += self.y_velocity

        return ret_val

    def launch(self):
        self.is_stuck = False

    def stick(self):
        self.is_stuck = True

    def h_reflection(self):
        self.y_velocity = -1 * self.y_velocity

    def v_reflection(self):
        self.x_velocity = -1 * self.x_velocity
