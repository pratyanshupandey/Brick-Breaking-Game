from powerup import *
import random


class Brick:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.length = BRICK_LEN
        self.char = BRICK_CHAR[0]

    def random_powers(self):
        val = random.randint(1, 6)
        if val == 1:
            return ExpandPaddle(self)
        elif val == 2:
            return ShrinkPaddle(self)
        elif val == 3:
            return BallMultiplier(self)
        elif val == 4:
            return FastBall(self)
        elif val == 5:
            return ThruBall(self)
        else:
            return PaddleGrab(self)

    @staticmethod
    def sort_bricks(collided_bricks, cur_ball):

        def y_sort(brick):
            return brick.y

        def x_sort(brick):
            return brick.x

        collided_bricks.sort(reverse=(cur_ball.y_velocity < 0), key=y_sort)
        collided_bricks.sort(reverse=(cur_ball.x_velocity < 0), key=x_sort)
        return collided_bricks[0]

    @staticmethod
    def br_count(bricks):
        count = 0
        for brick in bricks:
            if not isinstance(brick, UnbreakableBrick):
                count += 1
        return count

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
