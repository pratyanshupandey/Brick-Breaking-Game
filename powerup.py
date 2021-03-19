from config import *
import copy
from point import Point
from time import time


class PowerUp:

    def __init__(self, brick, ball):
        self.x = brick.x
        self.y = brick.y
        self.x_velocity = ball.x_velocity
        self.y_velocity = ball.y_velocity

    @staticmethod
    def power():
        print("Power Up Activated")

    @staticmethod
    def unpower():
        print("Power Up De-activated")

    def oldmove(self, paddle):
        ret_val = 0
        next_y = self.y + POWER_VEL

        if next_y == paddle.y and (paddle.x - paddle.length // 2) <= self.x <= (paddle.x + paddle.length // 2):
            ret_val = 1

        self.y += POWER_VEL

        if self.y >= SCREEN_ROWS - 1:
            ret_val = -1

        return ret_val

    def move(self, paddle):
        ret_val = 0
        collision = True
        cur_ball = Point(self.x, self.y)
        next_ball = Point(self.x + self.x_velocity, self.y + self.y_velocity)
        i = 0
        while collision and i < 10:
            collision = False
            i += 1

            # Collision with paddle
            paddle_left = Point(paddle.x - paddle.length // 2 - 0.5, paddle.y - 0.5)
            paddle_right = Point(paddle.x + paddle.length // 2 + 0.5, paddle.y - 0.5)
            if Point.is_intersecting(cur_ball, next_ball, paddle_left, paddle_right) and cur_ball.y != paddle_left.y:
                return 1

            # Collision with walls
            if next_ball.x <= 0.5:
                collision = True
                self.v_reflection(0.5, next_ball)
                cur_ball.x = 0.5
                cur_ball.y = Point.find_intersect_x(cur_ball, next_ball, cur_ball.x)

            if next_ball.x >= SCREEN_COLS - 1.5:
                collision = True
                self.v_reflection(SCREEN_COLS - 1.5, next_ball)
                cur_ball.x = SCREEN_COLS - 1.5
                cur_ball.y = Point.find_intersect_x(cur_ball, next_ball, cur_ball.x)

            if next_ball.y <= UPPER_WALL + 0.5:
                collision = True
                self.h_reflection(UPPER_WALL + 0.5, next_ball)
                cur_ball.y = UPPER_WALL + 0.5
                cur_ball.x = Point.find_intersect_y(cur_ball, next_ball, cur_ball.y)

            if next_ball.y >= SCREEN_ROWS - 1:
                ret_val = -1

        self.x = next_ball.x
        self.y = next_ball.y

        self.y_velocity = min(POWER_VEL_CAP, self.y_velocity + GRAVITY)
        return ret_val

    def h_reflection(self, y, next_ball):
        self.y_velocity = -1 * self.y_velocity
        next_ball.y = next_ball.y - 2 * (next_ball.y - y)

    def v_reflection(self, x, next_ball):
        self.x_velocity = -1 * self.x_velocity
        next_ball.x = next_ball.x - 2 * (next_ball.x - x)


class ExpandPaddle(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "E"
        self.color = POWER_COLOR['ExpandPaddle']

    @staticmethod
    def power(paddle, balls):
        paddle.length += PAD_LEN_EXTENSION
        return True

    @staticmethod
    def unpower(paddle, balls):
        paddle.length -= PAD_LEN_EXTENSION


class ShrinkPaddle(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "S"
        self.color = POWER_COLOR['ShrinkPaddle']

    @staticmethod
    def power(paddle, balls):
        if paddle.length > 3:
            paddle.length -= PAD_LEN_SHRINK
            return True
        return False

    @staticmethod
    def unpower(paddle, balls):
        paddle.length += PAD_LEN_SHRINK


class BallMultiplier(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "M"
        self.color = POWER_COLOR['BallMultiplier']

    @staticmethod
    def power(paddle, balls):
        new_balls = []
        for ball in balls:
            ball1 = copy.deepcopy(ball)
            ball1.x_velocity += 1
            ball2 = copy.deepcopy(ball)
            ball2.x_velocity -= 1
            new_balls.append(ball1)
            new_balls.append(ball2)
        return new_balls


class FastBall(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "F"
        self.color = POWER_COLOR['FastBall']

    @staticmethod
    def power(paddle, balls):
        for ball in balls:
            if ball.y_velocity > 0:
                ball.y_velocity += FAST_BALL_VEL
            else:
                ball.y_velocity -= FAST_BALL_VEL
        return True

    @staticmethod
    def unpower(paddle, balls):
        for ball in balls:
            if ball.y_velocity > 0:
                ball.y_velocity -= FAST_BALL_VEL
            else:
                ball.y_velocity += FAST_BALL_VEL


class ThruBall(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "T"
        self.color = POWER_COLOR['ThruBall']

    @staticmethod
    def power(paddle, balls):
        for ball in balls:
            ball.strength = MAX_BALL_STRENGTH
        return True

    @staticmethod
    def unpower(paddle, balls):
        for ball in balls:
            ball.strength = 1


class PaddleGrab(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "G"
        self.color = POWER_COLOR['PaddleGrab']

    @staticmethod
    def power(paddle, balls):
        paddle.is_sticky = True
        return True

    @staticmethod
    def unpower(paddle, balls):
        paddle.is_sticky = False


class ShootingPaddle(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "I"
        self.color = POWER_COLOR['ShootingPaddle']

    @staticmethod
    def power(paddle, balls):
        paddle.is_shooter = True
        paddle.last_bullet = time() - BULLET_TIMEOUT
        return True

    @staticmethod
    def unpower(paddle, balls):
        paddle.is_shooter = False


class FireBall(PowerUp):

    def __init__(self, brick, ball):
        super().__init__(brick, ball)
        self.char = "Y"
        self.color = POWER_COLOR["FireBall"]

    @staticmethod
    def power(paddle, balls):
        for ball in balls:
            ball.is_fireball = True
        return True

    @staticmethod
    def unpower(paddle, balls):
        for ball in balls:
            ball.is_fireball = False
        paddle.is_shooter = False
