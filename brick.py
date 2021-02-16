from config import *


class Brick:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = BRICK_LEN
        self.char = BRICK_CHAR[0]


class OneHitBrick(Brick):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = 1
        self.char = BRICK_CHAR[0]
        self.color = BRICK_COLOR[0]
        self.break_score = 10


class TwoHitBrick(Brick):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = 2
        self.char = BRICK_CHAR[1]
        self.color = BRICK_COLOR[1]
        self.break_score = 30


class ThreeHitBrick(Brick):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = 3
        self.char = BRICK_CHAR[2]
        self.color = BRICK_COLOR[2]
        self.break_score = 100


class UnbreakableBrick(Brick):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = MAX_BALL_STRENGTH - 1
        self.char = BRICK_CHAR[3]
        self.color = BRICK_COLOR[3]
        self.break_score = 200


class ExplodingBrick(Brick):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.strength = 1
        self.char = BRICK_CHAR[4]
        self.color = BRICK_COLOR[4]
        self.break_score = 30
