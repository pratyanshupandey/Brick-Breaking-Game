from point import *
from brick import *
from copy import deepcopy
from music import play_music


class Ball:

    def __init__(self):
        self.x = SCREEN_COLS // 2
        self.y = SCREEN_ROWS - 1 - PAD_VER_OFF
        self.is_stuck = True
        self.offset = int(random.randint(-1 * (PAD_LEN // 2), PAD_LEN // 2) * OFFSET_INCREASE)
        self.x_velocity = self.offset * BALL_VEL
        self.y_velocity = -1 * BALL_VEL
        self.strength = 1
        self.is_fireball = False

    @staticmethod
    def in_boss(cur_ball, next_ball, boss):
        boss_left = Point(boss.x - BOSS_WIDTH // 2 - 0.5, boss.y)
        boss_right = Point(boss.x + BOSS_WIDTH // 2 + 0.5, boss.y)
        if boss_left.x <= cur_ball.x <= boss_right.x and (boss.y - BOSS_HEIGHT // 2 - 0.5) <= cur_ball.y <= (
                boss.y + BOSS_HEIGHT // 2 + 0.5):
            if boss_left.x <= next_ball.x <= boss_right.x and (boss.y - BOSS_HEIGHT // 2 - 0.5) <= next_ball.y <= (
                    boss.y + BOSS_HEIGHT // 2 + 0.5):
                return True
            else:
                return False
        return False

    def move(self, paddle, bricks, boss, level, mode):
        old_ball = deepcopy(self)
        paddle_collision = False
        ret_val = True
        score = 0
        new_powers = []

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

                if Point.is_intersecting(cur_ball, next_ball, paddle_left,
                                         paddle_right) and cur_ball.y != paddle_left.y:
                    collision = True
                    paddle_collision = True
                    intersect = Point.find_intersect_y(cur_ball, next_ball, paddle.y)
                    self.offset = int((intersect - paddle.x) * OFFSET_INCREASE)

                    if paddle.is_sticky:
                        self.is_stuck = True
                        self.h_reflection(paddle_left.y, next_ball)

                    else:
                        self.h_reflection(paddle_left.y, next_ball)

                    self.x_velocity += self.offset * BALL_VEL
                    cur_ball.x = intersect
                    cur_ball.y = paddle_right.y

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
                    ret_val = False

                # Collision with boss in Boss level
                boss_collision = False
                if level == BOSS_LEVEL:
                    boss_left = Point(boss.x - BOSS_WIDTH // 2 - 0.5, boss.y)
                    boss_right = Point(boss.x + BOSS_WIDTH // 2 + 0.5, boss.y)
                    val = Point.rect_intersection(cur_ball, next_ball, boss_left, boss_right, BOSS_HEIGHT)
                    if val != 0 or Ball.in_boss(cur_ball, next_ball, boss):
                        collision = True
                        boss_collision = True

                # Collision with bricks
                collided_bricks = []
                for brick in bricks:
                    brick_left = Point(brick.x - brick.length // 2 - 0.5, brick.y)
                    brick_right = Point(brick.x + brick.length // 2 + 0.5, brick.y)
                    val = Point.rect_intersection(cur_ball, next_ball, brick_left, brick_right)

                    if val != 0:
                        collision = True
                        collided_bricks.append(brick)

                col_brick = None
                if len(collided_bricks) != 0:
                    col_brick = Brick.sort_bricks(collided_bricks, self)

                if col_brick is not None or boss_collision:
                    play_music("collision")
                    if col_brick is None:
                        collider = boss
                    elif not boss_collision:
                        collider = col_brick
                    elif boss.before_brick(cur_ball, col_brick):
                        collider = boss
                    else:
                        collider = col_brick

                    if isinstance(collider, Brick):
                        brick = collider
                        brick_left = Point(brick.x - brick.length // 2 - 0.5, brick.y)
                        brick_right = Point(brick.x + brick.length // 2 + 0.5, brick.y)
                        val = Point.rect_intersection(cur_ball, next_ball, brick_left, brick_right)
                        if isinstance(brick, RainbowBrick) and brick.is_changing:
                            brick.is_changing = False
                            brick.fix()
                        else:
                            brick.strength -= self.strength
                        if self.is_fireball:
                            brick.strength = 0
                            brick.is_fireballed = True

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
                                cur_ball.y = Point.find_intersect_x(cur_ball, next_ball, cur_ball.x)

                            elif val == 2:
                                self.h_reflection(brick.y + 0.5, next_ball)
                                cur_ball.y = brick.y + 0.5
                                cur_ball.x = Point.find_intersect_y(cur_ball, next_ball, cur_ball.y)

                            elif val == 3:
                                self.v_reflection(brick_right.x, next_ball)
                                cur_ball.x = brick_right.x
                                cur_ball.y = Point.find_intersect_x(cur_ball, next_ball, cur_ball.x)

                            elif val == 4:
                                self.h_reflection(brick.y - 0.5, next_ball)
                                cur_ball.y = brick.y - 0.5
                                cur_ball.x = Point.find_intersect_y(cur_ball, next_ball, cur_ball.y)

                            else:
                                pass
                    else:
                        boss_left = Point(boss.x - BOSS_WIDTH // 2 - 0.5, boss.y)
                        boss_right = Point(boss.x + BOSS_WIDTH // 2 + 0.5, boss.y)

                        if Ball.in_boss(cur_ball, next_ball, boss):
                            # file = open("log.txt", "a")
                            # file.write("In {} {} {} {}\n".format(cur_ball.x, cur_ball.y, next_ball.x, next_ball.y))
                            prev_ball = Point(2 * cur_ball.x - next_ball.x, 2 * cur_ball.y - next_ball.y)
                            if next_ball.x == cur_ball.x:
                                next_ball.x += 1
                                if cur_ball.x > boss.x:
                                    self.x_velocity += 1
                                else:
                                    self.x_velocity -= 1
                            else:
                                cur_ball = prev_ball
                            # file.write("In {} {} {} {}\n".format(cur_ball.x, cur_ball.y, next_ball.x, next_ball.y))
                            # file.close()

                        val = Point.rect_intersection(cur_ball, next_ball, boss_left, boss_right, BOSS_HEIGHT)
                        if val != 0:
                            boss.strength -= 1
                        if val == 1:
                            self.v_reflection(boss_left.x, next_ball)
                            cur_ball.x = boss_left.x
                            cur_ball.y = Point.find_intersect_x(cur_ball, next_ball, cur_ball.x)

                        elif val == 2:
                            self.h_reflection(boss.y + BOSS_HEIGHT // 2 + 0.5, next_ball)
                            cur_ball.y = boss.y + 0.5
                            cur_ball.x = Point.find_intersect_y(cur_ball, next_ball, cur_ball.y)

                        elif val == 3:
                            self.v_reflection(boss_right.x, next_ball)
                            cur_ball.x = boss_right.x
                            cur_ball.y = Point.find_intersect_x(cur_ball, next_ball, cur_ball.x)

                        elif val == 4:
                            self.h_reflection(boss.y - BOSS_HEIGHT // 2 - 0.5, next_ball)
                            cur_ball.y = boss.y - 0.5
                            cur_ball.x = Point.find_intersect_y(cur_ball, next_ball, cur_ball.y)

                        else:
                            pass

                # Creating powers from exploded bricks
                no_exploding_brick = True
                while no_exploding_brick:
                    no_exploding_brick = False
                    for brick in bricks:
                        if brick.strength <= 0:
                            score += brick.break_score
                            if random.randint(1, POWER_CHANCES) == 1:
                                new_powers.append(brick.random_powers(old_ball))
                            if isinstance(brick, ExplodingBrick) or brick.is_fireballed:
                                play_music("Explosion")
                                no_exploding_brick = True
                                for j in range(len(bricks)):
                                    if bricks[j].strength != 0 and abs(brick.y - bricks[j].y) <= 1 and abs(
                                            brick.x - bricks[j].x) <= BRICK_LEN:
                                        bricks[j].strength = 0
                            bricks.remove(brick)

            self.x = next_ball.x
            self.y = next_ball.y
        if mode == "Easy":
            if self.x_velocity < 0:
                self.x_velocity = max(self.x_velocity, -1 * X_CAPPED_VEL)
            else:
                self.x_velocity = min(self.x_velocity, X_CAPPED_VEL)

        return ret_val, score, new_powers, paddle_collision

    def launch(self):
        self.is_stuck = False

    def stick(self):
        self.is_stuck = True

    def h_reflection(self, y, next_ball):
        self.y_velocity = -1 * self.y_velocity
        next_ball.y = next_ball.y - 2 * (next_ball.y - y)

    def v_reflection(self, x, next_ball):
        self.x_velocity = -1 * self.x_velocity
        next_ball.x = next_ball.x - 2 * (next_ball.x - x)
