import os


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Class for creating a point object for purpose of collision detection
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Checks if r is on pq
    @staticmethod
    def r_on_pq(p, r, q):

        if (max(p.x, q.x) >= r.x) and\
                (min(p.x, q.x) <= r.x) and\
                (max(p.y, q.y) >= r.y) and\
                (min(p.y, q.y) <= r.y):
            return True
        return False

    # 0 = Collinear 1 = Clockwise 2 = Anti-Clockwise
    @staticmethod
    def tp_orient(p, q, r):
        val1 = float(q.y - p.y) * float(r.x - q.x)
        val2 = float(q.x - p.x) * float(r.y - q.y)
        if val1 == val2:
            return 0
        elif val1 > val2:
            return 1
        else:
            return 2

    # Check if p1q1 and p2q2 intersect
    @staticmethod
    def is_intersecting(p1, q1, p2, q2):
        orientation1 = Point.tp_orient(p1, q1, p2)
        orientation2 = Point.tp_orient(p1, q1, q2)
        orientation3 = Point.tp_orient(p2, q2, p1)
        orientation4 = Point.tp_orient(p2, q2, q1)

        if ((orientation1 != orientation2) and (orientation3 != orientation4)) or \
                ((orientation1 == 0) and Point.r_on_pq(p1, p2, q1)) or \
                ((orientation2 == 0) and Point.r_on_pq(p1, q2, q1)) or \
                ((orientation3 == 0) and Point.r_on_pq(p2, p1, q2)) or \
                ((orientation4 == 0) and Point.r_on_pq(p2, q1, q2)):
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
    def rect_intersection(cur_ball, next_ball, brick_left, brick_right, height=0):
        # file = open("log.txt", "a")

        right_wall_top = Point(brick_right.x, brick_right.y - height//2 - 0.5)
        right_wall_bottom = Point(brick_right.x, brick_right.y + height//2 + 0.5)

        left_wall_top = Point(brick_left.x, brick_left.y - height//2- 0.5)
        left_wall_bottom = Point(brick_left.x, brick_left.y + height//2 + 0.5)

        left = Point.is_intersecting(cur_ball, next_ball, left_wall_top, left_wall_bottom)
        right = Point.is_intersecting(cur_ball, next_ball, right_wall_top, right_wall_bottom)
        top = Point.is_intersecting(cur_ball, next_ball, right_wall_top, left_wall_top)
        bottom = Point.is_intersecting(cur_ball, next_ball, left_wall_bottom, right_wall_bottom)

        # file.write("{} {} {} {}\n".format(right_wall_top.x, right_wall_top.y, right_wall_bottom.x, right_wall_bottom.y))
        # file.write("{} {} {} {}\n".format(cur_ball.x, cur_ball.y, next_ball.x, next_ball.y))
        # file.write("{} {} {} {}\n\n".format(left,right,top,bottom))
        # file.close()
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
