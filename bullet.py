from config import *
import random
from point import Point
from brick import ExplodingBrick, Brick, RainbowBrick


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_velocity = 0
        self.y_velocity = BULLET_SPEED
        self.char = BULLET_CHAR
        self.color = BULLET_COLOR
        self.strength = 1

    def move(self, bricks):
        ret_val = 0
        score = 0

        cur_bullet = Point(self.x, self.y)
        next_bullet = Point(self.x + self.x_velocity, self.y + self.y_velocity)

        # Collision with walls
        if next_bullet.x <= 0.5:
            return -1, 0
        if next_bullet.x >= SCREEN_COLS - 1.5:
            return -1, 0
        if next_bullet.y <= UPPER_WALL + 0.5:
            return -1, 0
        if next_bullet.y >= SCREEN_ROWS - 1:
            return -1, 0

        # Collision with bricks
        collided_bricks = []
        for brick in bricks:
            brick_left = Point(brick.x - brick.length // 2 - 0.5, brick.y)
            brick_right = Point(brick.x + brick.length // 2 + 0.5, brick.y)
            val = Point.rect_intersection(cur_bullet, next_bullet, brick_left, brick_right)

            if val != 0:
                collided_bricks.append(brick)

        if len(collided_bricks) != 0:
            ret_val = -1
            brick = Brick.sort_bricks(collided_bricks, self)

            if isinstance(brick, RainbowBrick) and brick.is_changing:
                brick.is_changing = False
                brick.fix()
            else:
                brick.strength -= self.strength

            if brick.strength <= 0:
                pass

            else:
                if brick.strength >= 4:
                    pass
                else:
                    brick.char = BRICK_CHAR[brick.strength - 1]
                    brick.color = BRICK_COLOR[brick.strength - 1]

        # Creating powers from exploded bricks
        no_exploding_brick = True
        while no_exploding_brick:
            no_exploding_brick = False
            for brick in bricks:
                if brick.strength <= 0:
                    score += brick.break_score
                    if isinstance(brick, ExplodingBrick):
                        no_exploding_brick = True
                        for j in range(len(bricks)):
                            if bricks[j].strength != 0 and abs(brick.y - bricks[j].y) <= 1 and abs(
                                    brick.x - bricks[j].x) <= BRICK_LEN:
                                bricks[j].strength = 0
                    bricks.remove(brick)

        self.x = next_bullet.x
        self.y = next_bullet.y

        return ret_val, score

    def h_reflection(self, y, next_bullet):
        self.y_velocity = -1 * self.y_velocity
        next_bullet.y = next_bullet.y - 2 * (next_bullet.y - y)

    def v_reflection(self, x, next_bullet):
        self.x_velocity = -1 * self.x_velocity
        next_bullet.x = next_bullet.x - 2 * (next_bullet.x - x)
