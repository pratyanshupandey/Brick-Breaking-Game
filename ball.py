from utils import *

class Ball:

    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = SCREEN_ROWS - 4
        self.is_stuck = True
        self.offset = 0
        # self.offset = random.randint(-1 * (PAD_LEN // 2), PAD_LEN // 2)
        self.x_velocity = self.offset * BALL_VEL
        self.y_velocity = -1 * BALL_VEL
        self.strength = 1
        self.x = 33
        self.y = 34
        self.x_velocity = 0
        self.y_velocity = 1

    def move(self, paddle, bricks):
        ret_val = True
        score = 0
        new_powers = []
        is_paddle_col = False

        file = open("demofile3.txt", "a")
        if self.is_stuck:
            self.x = paddle.x + self.offset

        else:
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
                if doIntersect(cur_ball, next_ball, paddle_left, paddle_right) and cur_ball.y != paddle_left.y:
                    file.write("before coll = {} {} {} {} {} {}\n".format(cur_ball.x, cur_ball.y, next_ball.x, next_ball.y, paddle.x, paddle.y))
                    is_paddle_col  = True
                    collision = True

                    # file.write("intersect = {} {} {} paddle = {}\n".format(find_intersect_y(cur_ball, next_ball, paddle_left.y), next_ball.x, next_ball.y, paddle.x))
                    intersect = find_intersect_y(cur_ball, next_ball, paddle.y)
                    self.offset = (intersect - paddle.x) * OFFSET_INCREASE

                    if paddle.is_sticky:
                        self.is_stuck = True
                        self.h_reflection(paddle_left.y, next_ball)
                    else:
                        self.h_reflection(paddle_left.y, next_ball)
                    # file.write("after coll = {} {} {} {}\n".format(next_ball.x, next_ball.y, paddle.x, paddle.y))
                    file.write("OFFSET = {}\n".format(self.offset))
                    self.x_velocity += self.offset * BALL_VEL

                    cur_ball.x = intersect
                    cur_ball.y = paddle_right.y
                    file.write("after coll = {} {} {} {} {} {}\n".format(cur_ball.x, cur_ball.y, next_ball.x, next_ball.y, paddle.x, paddle.y))


                # Collision with walls
                if next_ball.x <= 0.5:
                    collision = True
                    self.v_reflection(0.5, next_ball)
                    cur_ball.x = 0.5
                    cur_ball.y = find_intersect_x(cur_ball,next_ball,cur_ball.x)

                if next_ball.x >= SCREEN_COLS - 1.5:
                    collision = True
                    self.v_reflection(SCREEN_COLS - 1.5, next_ball)
                    cur_ball.x = SCREEN_COLS - 1.5
                    cur_ball.y = find_intersect_x(cur_ball, next_ball, cur_ball.x)

                if next_ball.y <= UPPER_WALL + 0.5:
                    collision = True
                    self.h_reflection(UPPER_WALL + 0.5, next_ball)
                    cur_ball.y = UPPER_WALL + 0.5
                    cur_ball.x = find_intersect_y(cur_ball, next_ball, cur_ball.y)

                if next_ball.y >= SCREEN_ROWS - 1:
                    ret_val = False


                # Collision with bricks
                collided_bricks = []
                # file.write("before brick coll = {} {} {} {}\n".format(next_ball.x, next_ball.y, cur_ball.x, cur_ball.y))
                for brick in bricks:
                    brick_left = Point(brick.x - brick.length // 2 - 0.5, brick.y)
                    brick_right = Point(brick.x + brick.length // 2 + 0.5, brick.y)
                    val = rect_intersection(cur_ball, next_ball, brick_left, brick_right)
                    # if doIntersect(cur_ball, next_ball, brick_left, brick_right) and self.y != brick.y:
                    if val != 0:
                        collision = True
                        collided_bricks.append(brick)
                        # file.write("Col Brick char = {} {} {}\n".format(brick.char , brick.x, brick.y))

                if len(collided_bricks) != 0:
                    brick = sort_bricks(collided_bricks, self)
                    brick_left = Point(brick.x - brick.length // 2 - 0.5, brick.y)
                    brick_right = Point(brick.x + brick.length // 2 + 0.5, brick.y)
                    val = rect_intersection(cur_ball, next_ball, brick_left, brick_right)
                    brick.strength -= self.strength
                    if brick.strength <= 0:
                        pass
                    else:
                        if brick.strength >= 4:
                            pass
                        else:
                            brick.char = BRICK_CHAR[brick.strength - 1]
                            brick.color = BRICK_COLOR[brick.strength - 1]

                    if self.strength == MAX_BALL_STRENGTH:
                        pass
                    else:
                        if val == 1:
                            self.v_reflection(brick_left.x, next_ball)
                            cur_ball.x = brick_left.x
                            cur_ball.y = find_intersect_x(cur_ball, next_ball, cur_ball.x)

                        elif val == 2:
                            self.h_reflection(brick.y + 0.5, next_ball)
                            cur_ball.y = brick.y + 0.5
                            cur_ball.x = find_intersect_y(cur_ball, next_ball, cur_ball.y)
                        elif val == 3:
                            self.v_reflection(brick_right.x, next_ball)
                            cur_ball.x = brick_right.x
                            cur_ball.y = find_intersect_x(cur_ball, next_ball, cur_ball.x)
                        elif val == 4:
                            self.h_reflection(brick.y - 0.5, next_ball)
                            cur_ball.y = brick.y - 0.5
                            cur_ball.x = find_intersect_y(cur_ball, next_ball, cur_ball.y)
                        else:
                            pass
                        # file.write("after brick coll = {} {} {} {}\n".format(next_ball.x, next_ball.y, cur_ball.x,
                        #                                                           cur_ball.y))

                            # col = is_vertical(cur_ball, next_ball, brick_left, brick_right) # 0 = h 1 = r 2 = l
                            # file.write("col = {}\n".format(col))
                            # if col == 1:
                            #     self.v_reflection(brick_right.x,next_ball)
                            # elif col == 2:
                            #     self.v_reflection(brick_left.x, next_ball)
                            # else:
                            #     self.h_reflection(brick.y, next_ball)
                            # break

                # Creating powerups from exploded bricks
                no_exploding_brick = True
                while no_exploding_brick:
                    no_exploding_brick = False
                    for brick in bricks:
                        if brick.strength <= 0:
                            score += brick.break_score
                            if random.randint(1, POWER_CHANCES) == 1:
                                new_powers.append(random_powers(brick))
                            if isinstance(brick, ExplodingBrick):
                                no_exploding_brick = True
                                for j in range(len(bricks)):
                                    if bricks[j].strength != 0 and abs(brick.y - bricks[j].y) <= 1 and abs(
                                            brick.x - bricks[j].x) == BRICK_LEN:
                                        bricks[j].strength = 0
                            bricks.remove(brick)

                # next_x = self.x + self.x_velocity
                # next_y = self.y + self.y_velocity
                #
                # if next_x <= 0 or next_x >= SCREEN_COLS - 1:
                #     self.v_reflection()
                #
                # if next_y <= UPPER_WALL:
                #     self.h_reflection()
                #
                # if next_y >= SCREEN_ROWS - 1:
                #     ret_val = False
                #
                # if next_y == paddle.y and (paddle.x - paddle.length // 2) <= next_x <= (paddle.x + paddle.length // 2):
                #     self.y_velocity = -1 * self.y_velocity
                #     self.x_velocity += next_x - paddle.x

            self.x = next_ball.x
            self.y = next_ball.y

        file.write("{} {} {} {}\n".format(self.x, self.y, self.x_velocity, self.y_velocity))
        file.close()
        # if is_paddle_col:
        #     self.x_velocity += self.offset * BALL_VEL
        return ret_val, score, new_powers

    def launch(self):
        self.is_stuck = False

    def stick(self):
        self.is_stuck = True

    def h_reflection(self , y, next_ball):
        self.y_velocity = -1 * self.y_velocity
        next_ball.y = next_ball.y - 2 * (next_ball.y - y)

    def v_reflection(self, x, next_ball):
        self.x_velocity = -1 * self.x_velocity
        next_ball.x = next_ball.x - 2 * (next_ball.x - x)
