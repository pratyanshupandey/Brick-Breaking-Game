from config import *
import copy


class PowerUp:

    def __init__(self, brick):
        self.x = brick.x
        self.y = brick.y

    def move(self,paddle):
        ret_val = 0
        next_y = self.y + POWER_VEL

        if next_y == paddle.y and (paddle.x - paddle.length // 2) <= self.x <= (paddle.x + paddle.length // 2):
            ret_val = 1

        self.y += POWER_VEL

        if self.y >= SCREEN_ROWS - 1:
            ret_val = -1

        return ret_val


class ExpandPaddle(PowerUp):

    def __init__(self, brick):
        super().__init__(brick)
        self.char = "E"

    def power(self, paddle, balls):
        paddle.length += PAD_LEN_EXTENSION
        return True

    def unpower(self, paddle, balls):
        paddle.length -= PAD_LEN_EXTENSION


class ShrinkPaddle(PowerUp):

    def __init__(self, brick):
        super().__init__(brick)
        self.char = "S"

    def power(self, paddle, balls):
        if paddle.length > 3:
            paddle.length -= PAD_LEN_SHRINK
            return True
        return False

    def unpower(self, paddle, balls):
        paddle.length += PAD_LEN_SHRINK


class BallMultiplier(PowerUp):

    def __init__(self, brick):
        super().__init__(brick)
        self.char = "M"

    def power(self, paddle, balls):
        new_balls = []
        for ball in balls:
            ball1 = copy.deepcopy(ball)
            ball1.x_velocity += 1
            ball2 = copy.deepcopy(ball)
            ball1.x_velocity -= 1
            new_balls.append(ball1)
            new_balls.append(ball2)
        return new_balls


class FastBall(PowerUp):

    def __init__(self, brick):
        super().__init__(brick)
        self.char = "F"

    def power(self, paddle, balls):
        for ball in balls:
            if ball.y_velocity > 0:
                ball.y_velocity += FAST_BALL_VEL
            else:
                ball.y_velocity -= FAST_BALL_VEL
        return True

    def unpower(self, paddle, balls):
        for ball in balls:
            if ball.y_velocity > 0:
                ball.y_velocity -= FAST_BALL_VEL
            else:
                ball.y_velocity += FAST_BALL_VEL


class ThruBall(PowerUp):

    def __init__(self, brick):
        super().__init__(brick)
        self.char = "T"

    def power(self, paddle, balls):
        for ball in balls:
            ball.strength = MAX_BALL_STRENGTH
        return True

    def unpower(self, paddle, balls):
        for ball in balls:
            ball.strength = 1


class PaddleGrab(PowerUp):

    def __init__(self, brick):
        super().__init__(brick)
        self.char = "G"

    def power(self, paddle, balls):
        for ball in balls:
            ball.is_stuck = True
        return True

    def unpower(self, paddle, balls):
        for ball in balls:
            ball.is_stuck = False
