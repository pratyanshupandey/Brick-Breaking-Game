import os
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

# pq line with y = y
def find_intersect_y(p,q, y):
    if p.x == q.x:
        return p.x
    else:
        val = (y - p.y) * (q.x - p.x) / (q.y - p.y) + p.x
        return val

# pq line with x = x
def find_intersect_x(p,q, x):
    if p.y == q.y:
        return p.y
    elif p.x == q.x:
        return (p.y + q.y) / 2
    else:
        val = p.y + (q.y - p.y)*(x - p.x)/(q.x - p.x)
        return val



# 0 = h 1 = r 2 = l
def is_vertical(cur_ball, next_ball, brick_left, brick_right):
    if next_ball.x == cur_ball.x:
        return 0
    right_wall_top = Point(brick_right.x, brick_right.y - 0.5)
    right_wall_bottom = Point(brick_right.x, brick_right.y + 0.5)
    if doIntersect(cur_ball, next_ball, right_wall_top, right_wall_bottom):
        return 1
    left_wall_top = Point(brick_left.x, brick_left.y - 0.5)
    left_wall_bottom = Point(brick_left.x, brick_left.y + 0.5)
    if doIntersect(cur_ball, next_ball, left_wall_top, left_wall_bottom):
        return 2
    return 0


#          4
#   ___________
# 1 |         | 3
#   ___________
#       2           0 = No intersection

def rect_intersection(cur_ball, next_ball, brick_left, brick_right):
    right = False
    left = False
    top = False
    bottom = False
    right_wall_top = Point(brick_right.x, brick_right.y - 0.5)
    right_wall_bottom = Point(brick_right.x, brick_right.y + 0.5)

    left_wall_top = Point(brick_left.x, brick_left.y - 0.5)
    left_wall_bottom = Point(brick_left.x, brick_left.y + 0.5)

    left = doIntersect(cur_ball, next_ball, left_wall_top, left_wall_bottom)
    right = doIntersect(cur_ball, next_ball, right_wall_top, right_wall_bottom)
    top = doIntersect(cur_ball, next_ball, right_wall_top, left_wall_top)
    bottom = doIntersect(cur_ball, next_ball, left_wall_bottom, right_wall_bottom)

    if left and cur_ball.x < brick_left.x:
        return 1
    if right and cur_ball.x > brick_right.x:
        return 3
    if top and cur_ball.y < left_wall_top.y:
        return 4
    if bottom and cur_ball.y > left_wall_bottom.y:
        return 2
    return 0

def distance(x1,y1,x2,y2):
    val = (x2 - x1)**2 + (y2 - y1)**2
    return val

# def sort_bricks(collided_bricks, cur_ball):
#     ret_brick = collided_bricks[0]
#     for brick in collided_bricks:
#         if distance(cur_ball.x, cur_ball.y, brick.x, brick.y) < distance(cur_ball.x, cur_ball.y, ret_brick.x, ret_brick.y):
#             ret_brick = brick
#     return ret_brick

def y_sort(brick):
    return brick.y


def x_sort(brick):
    return brick.x


def sort_bricks(collided_bricks, cur_ball):
    collided_bricks.sort(reverse=(cur_ball.y_velocity < 0), key=y_sort)
    collided_bricks.sort(reverse=(cur_ball.x_velocity < 0), key=x_sort)
    return collided_bricks[0]

def get_score_grid(score, time, lives, powers, cur_time):
    score_line = []
    score_line.append(SCREEN_BORDER + "|")
    score_str = "  SCORE = {}   TIME = {}   LIVES = {}".format(score,time,lives)
    for i in range(SCREEN_COLS - 2 - len(score_str)):
        score_str += " "
    score_line.append(SCREEN_BG + score_str)
    score_line.append(SCREEN_BORDER + "|")

    power_line = []
    power_line.append(SCREEN_BORDER + "|")
    power_str = "  POWERUPS = "
    for tim, power in powers:
        power_str += ("{}({}) ".format(power.__class__.__name__, POWER_TIMEOUT - int(cur_time - tim)))
    for i in range(SCREEN_COLS - 2 - len(power_str)):
        power_str += " "
    power_line.append(DATA_COLOR + power_str)
    power_line.append(SCREEN_BORDER + "|")

    return score_line, power_line
