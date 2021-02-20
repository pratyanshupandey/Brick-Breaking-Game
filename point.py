import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Class for creating a point object for purpose of collision detection
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Checks if q is on pr
    @staticmethod
    def q_on_pr(p, q, r):
        if ((q.x <= max(p.x, r.x)) and (q.x >= min(p.x, r.x)) and
                (q.y <= max(p.y, r.y)) and (q.y >= min(p.y, r.y))):
            return True
        return False

    # 0 = Collinear 1 = Clockwise 2 = Anti-Clockwise
    @staticmethod
    def orientation(p, q, r):
        val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
        if val > 0:
            return 1
        elif val < 0:
            return 2
        else:
            return 0

    # Check if p1q1 and p2q2 intersect
    @staticmethod
    def is_intersecting(p1, q1, p2, q2):
        o1 = Point.orientation(p1, q1, p2)
        o2 = Point.orientation(p1, q1, q2)
        o3 = Point.orientation(p2, q2, p1)
        o4 = Point.orientation(p2, q2, q1)

        if (o1 != o2) and (o3 != o4):
            return True

        if (o1 == 0) and Point.q_on_pr(p1, p2, q1):
            return True

        if (o2 == 0) and Point.q_on_pr(p1, q2, q1):
            return True

        if (o3 == 0) and Point.q_on_pr(p2, p1, q2):
            return True

        if (o4 == 0) and Point.q_on_pr(p2, q1, q2):
            return True

        return False

    # pq line with y = y
    @staticmethod
    def find_intersect_y(p, q, y):
        if p.x == q.x:
            return p.x
        else:
            val = (y - p.y) * (q.x - p.x) / (q.y - p.y) + p.x
            return val

    # pq line with x = x
    @staticmethod
    def find_intersect_x(p, q, x):
        if p.y == q.y:
            return p.y
        elif p.x == q.x:
            return (p.y + q.y) / 2
        else:
            val = p.y + (q.y - p.y) * (x - p.x) / (q.x - p.x)
            return val

    # 0 = h 1 = r 2 = l
    @staticmethod
    def is_vertical(cur_ball, next_ball, brick_left, brick_right):
        if next_ball.x == cur_ball.x:
            return 0
        right_wall_top = Point(brick_right.x, brick_right.y - 0.5)
        right_wall_bottom = Point(brick_right.x, brick_right.y + 0.5)
        if Point.is_intersecting(cur_ball, next_ball, right_wall_top, right_wall_bottom):
            return 1
        left_wall_top = Point(brick_left.x, brick_left.y - 0.5)
        left_wall_bottom = Point(brick_left.x, brick_left.y + 0.5)
        if Point.is_intersecting(cur_ball, next_ball, left_wall_top, left_wall_bottom):
            return 2
        return 0

    #          4
    #   ___________
    # 1 |         | 3
    #   ___________
    #       2           0 = No intersection
    @staticmethod
    def rect_intersection(cur_ball, next_ball, brick_left, brick_right):
        right_wall_top = Point(brick_right.x, brick_right.y - 0.5)
        right_wall_bottom = Point(brick_right.x, brick_right.y + 0.5)

        left_wall_top = Point(brick_left.x, brick_left.y - 0.5)
        left_wall_bottom = Point(brick_left.x, brick_left.y + 0.5)

        left = Point.is_intersecting(cur_ball, next_ball, left_wall_top, left_wall_bottom)
        right = Point.is_intersecting(cur_ball, next_ball, right_wall_top, right_wall_bottom)
        top = Point.is_intersecting(cur_ball, next_ball, right_wall_top, left_wall_top)
        bottom = Point.is_intersecting(cur_ball, next_ball, left_wall_bottom, right_wall_bottom)

        if left and cur_ball.x < brick_left.x:
            return 1
        if right and cur_ball.x > brick_right.x:
            return 3
        if top and cur_ball.y < left_wall_top.y:
            return 4
        if bottom and cur_ball.y > left_wall_bottom.y:
            return 2
        return 0

    @staticmethod
    def distance(x1, y1, x2, y2):
        val = (x2 - x1) ** 2 + (y2 - y1) ** 2
        return val

# def sort_bricks(collided_bricks, cur_ball):
#     ret_brick = collided_bricks[0]
#     for brick in collided_bricks:
#         if Point.distance(cur_ball.x, cur_ball.y, brick.x, brick.y) < Point.distance(cur_ball.x, cur_ball.y,
#                                                                                      ret_brick.x,
#                                                                                      ret_brick.y):
#             ret_brick = brick
#     return ret_brick
