from powerup import *
import random


class Brick:

    def __init__(self, x, y, index):
        self.x = x
        self.y = y
        self.length = BRICK_LEN
        self.strength = BRICK_STRENGTH[index]
        self.char = BRICK_CHAR[index]
        self.color = BRICK_COLOR[index]
        self.break_score = BRICK_BREAK_SCORE[index]

    def random_powers(self, ball):
        val = random.randint(1, 6)
        if val == 1:
            return ExpandPaddle(self, ball)
        elif val == 2:
            return ShrinkPaddle(self, ball)
        elif val == 3:
            return BallMultiplier(self, ball)
        elif val == 4:
            return FastBall(self, ball)
        elif val == 5:
            return ThruBall(self, ball)
        else:
            return PaddleGrab(self, ball)

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
        self.index = 0
        super().__init__(x, y, self.index)


class TwoHitBrick(Brick):

    def __init__(self, x, y):
        self.index = 1
        super().__init__(x, y, self.index)


class ThreeHitBrick(Brick):

    def __init__(self, x, y):
        self.index = 2
        super().__init__(x, y, self.index)


class UnbreakableBrick(Brick):

    def __init__(self, x, y):
        self.index = 3
        super().__init__(x, y, self.index)


class ExplodingBrick(Brick):

    def __init__(self, x, y):
        self.index = 4
        super().__init__(x, y, self.index)


class RainbowBrick(Brick):

    def __init__(self, x, y):
        self.index = 0
        super().__init__(x, y, self.index)
        self.is_changing = True

    def alter(self):
        self.index = (self.index + 1) % 4
        super().__init__(self.x, self.y, self.index)

    def replace(self):
        if self.index == 0:
            return OneHitBrick(self.x, self.y)
        elif self.index == 1:
            return TwoHitBrick(self.x, self.y)
        elif self.index == 3:
            return ThreeHitBrick(self.x, self.y)
        elif self.index == 0:
            return UnbreakableBrick(self.x, self.y)
        elif self.index == 0:
            return ExplodingBrick(self.x, self.y)
