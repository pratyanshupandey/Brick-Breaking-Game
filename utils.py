import os
from config import *
from powerup import *
import random
from brick import ExplodingBrick


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def random_powers(brick):
    val = random.randint(5,5)
    if val == 1:
        return ExpandPaddle(brick)
    elif val == 2:
        return ShrinkPaddle(brick)
    elif val == 3:
        return BallMultiplier(brick)
    elif val == 4:
        return FastBall(brick)
    elif val == 5:
        return ThruBall(brick)
    else:
        return PaddleGrab(brick)


def ball_brick_collision(balls, bricks):
    score = 0
    for ball in balls:
        next_y = ball.y + ball.y_velocity
        next_x = ball.x + ball.x_velocity
        for brick in bricks:
            if next_y == brick.y and (brick.x - brick.length // 2) <= next_x <= (brick.x + brick.length // 2):
                brick.strength -= ball.strength
                if brick.strength <= 0:
                    pass
                else:
                    if brick.strength >= 4:
                        pass
                    else:
                        brick.char = BRICK_CHAR[brick.strength - 1]
                        brick.color = BRICK_COLOR[brick.strength - 1]

                if ball.strength == MAX_BALL_STRENGTH:
                    pass
                else:
                    if next_x == (brick.x - brick.length // 2):
                        if ball.x < next_x:
                            ball.v_reflection()
                        else:
                            ball.h_reflection()

                    elif next_x == (brick.x + brick.length // 2):
                        if ball.x > next_x:
                            ball.v_reflection()
                        else:
                            ball.h_reflection()
                    else:
                        ball.h_reflection()
                    break

    new_powers = []
    # for i in range(len(bricks)):
    #     brick = bricks[i]
    no_exploding_brick = True
    while no_exploding_brick:
        no_exploding_brick=False
        for brick in bricks:
            if brick.strength <= 0:
                score += brick.break_score
                if random.randint(1, POWER_CHANCES) == 1:
                    new_powers.append(random_powers(brick))
                if isinstance(brick, ExplodingBrick):
                    no_exploding_brick=  True
                    for j in range(len(bricks)):
                        if bricks[j].strength != 0 and abs(brick.y - bricks[j].y) <= 1 and abs(brick.x - bricks[j].x) == BRICK_LEN:
                            bricks[j].strength = 0
                bricks.remove(brick)


    return score, new_powers


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Given three colinear points p, q, r, the function checks if


# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
            (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
        return True
    return False


def orientation(p, q, r):

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:
        # Clockwise orientation
        return 1
    elif val < 0:
        # Counterclockwise orientation
        return 2
    else:
        # Colinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def doIntersect(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False
