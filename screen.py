from paddle import Paddle
from ball import Ball
from point import *
from input import get_input
from bullet import *
from boss import Boss
from brick_layouts import *
from powerup import *
import termios
import sys
from music import play_music
from colorama import init, deinit, Style


class Game:
    def __init__(self, mode):
        self.mode = mode
        self.boss = Boss()
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.bullets = []
        self.bombs = []
        self.visible_powers = []
        self.active_powers = []
        self.level = 1
        self.bricks = load_layout(self.level)
        self.grid = []
        self.is_running = True
        self.quit = False
        self.lives = LIVES
        self.score = 0
        self.start_time = time()

    def start(self):
        total_time = 0
        while self.lives > 0 and self.level < 5:
            # -1 quit game
            # 0 all bricks done
            # 1 no ball left
            # 2 next level skip
            total_time += time() - self.start_time
            self.start_time = time()
            val = self.loop()
            if val == -1:
                break
            elif val == 0 or val == 2:
                self.level += 1
                play_music("NewLevel")
                self.bricks = load_layout(self.level)
            elif val == 1:
                self.lives -= 1
                play_music("LifeLost")

            self.balls = [Ball()]
            self.visible_powers = []
            self.active_powers = []
            self.paddle = Paddle()
            self.bullets = []

        return self.score, int(total_time)

    def loop(self):

        # Taking Input
        while True:
            inputs = get_input()
            for inp in inputs:
                if inp == "a" or inp == "d":
                    self.paddle.move(inp)
                elif inp == "x":
                    for ball in self.balls:
                        ball.launch()
                elif inp == "q":
                    return -1
                elif inp == "n":
                    return 2
                else:
                    pass

            # Move the boss
            if self.level == BOSS_LEVEL:
                bomb = self.boss.move(self.paddle)
                if bomb is not None:
                    self.bombs.append(bomb)

            # Create Bullets
            if self.paddle.is_shooter and time() - self.paddle.last_bullet > BULLET_TIMEOUT:
                self.bullets.append(Bullet(self.paddle.x - self.paddle.length // 2, self.paddle.y))
                self.bullets.append(Bullet(self.paddle.x + self.paddle.length // 2, self.paddle.y))
                self.paddle.last_bullet = time()

            # Bullets
            for bullet in self.bullets:
                ret_val, score, new_powers = bullet.move(self.bricks)
                if ret_val == -1:
                    self.bullets.remove(bullet)
                self.score += score
                if self.level != BOSS_LEVEL:
                    for power in new_powers:
                        self.visible_powers.append(power)

            # handling bombs of boss level
            for bomb in self.bombs:
                val = bomb.move(self.paddle)
                if val == -1:
                    self.bombs.remove(bomb)
                elif val == 1:
                    self.lives -= 1
                    play_music("LifeLost")
                    self.bombs.remove(bomb)
                else:
                    pass

            # Moving Balls, Checking Collisions and Creating Powers
            paddle_collision = False
            for ball in self.balls:
                is_ball, add_score, new_powers, paddle_col = ball.move(self.paddle, self.bricks, self.boss, self.level,
                                                                       self.mode)
                paddle_collision |= paddle_col
                if not is_ball:
                    self.balls.remove(ball)
                self.score += add_score
                if self.level != BOSS_LEVEL:
                    for power in new_powers:
                        self.visible_powers.append(power)
            if paddle_collision:
                play_music("collision")

            # Managing Powers
            for power in self.visible_powers:
                val = power.move(self.paddle)
                if val == 1:
                    play_music("PowerupCatch")
                    if isinstance(power, BallMultiplier):
                        self.balls = power.power(self.paddle, self.balls)
                    elif power.power(self.paddle, self.balls):
                        if isinstance(power, PaddleGrab) and self.paddle.is_sticky:
                            for i in range(len(self.active_powers)):
                                if isinstance(self.active_powers[i][1], PaddleGrab):
                                    self.active_powers.remove(self.active_powers[i])
                                    break
                        self.active_powers.append((time(), power))
                    self.visible_powers.remove(power)
                elif val == -1:
                    self.visible_powers.remove(power)
                else:
                    pass

            for i in range(len(self.bricks)):
                if isinstance(self.bricks[i], RainbowBrick):
                    if self.bricks[i].is_changing:
                        self.bricks[i].alter()
                    # else:
                    #     self.bricks[i] = self.bricks[i].replace()

            for start_time, power in self.active_powers:
                if time() - start_time >= POWER_TIMEOUT:
                    for _, pow in self.active_powers:
                        if pow != power and type(pow) is type(power):
                            break
                    else:
                        power.unpower(self.paddle, self.balls)
                    self.active_powers.remove((start_time, power))

            if self.level != BOSS_LEVEL and time() - self.start_time > FALLING_BRICKS_TIMEOUT[self.level]:
                for brick in self.bricks:
                    if paddle_collision:
                        brick.y += 1
                    if brick.y >= SCREEN_ROWS - PAD_VER_OFF:
                        return -1

            if self.level == BOSS_LEVEL and self.boss.strength == BOSS_BRICK1 and self.boss.brick_left == 2:
                self.bricks.extend(boss_brick_1())
                self.boss.brick_left -= 1
            if self.level == BOSS_LEVEL and self.boss.strength == BOSS_BRICK2 and self.boss.brick_left == 1:
                self.bricks.extend(boss_brick_2())
                self.boss.brick_left -= 1

            if self.level != BOSS_LEVEL and Brick.br_count(self.bricks) == 0:
                return 0
            if self.level == BOSS_LEVEL and self.boss.strength == 0:
                self.score += BOSS_SCORE
                return 0
            elif len(self.balls) == 0:
                return 1
            elif self.lives <= 0:
                return -1

            self.create_grid()
            self.print_grid()

    def create_grid(self):
        self.grid = []
        for i in range(SCREEN_ROWS):
            self.grid.append([])
            for j in range(SCREEN_COLS):
                self.grid[i].append(SCREEN_BG + " ")

        # Screen Box
        for i in range(SCREEN_COLS):
            self.grid[0][i] = SCREEN_BORDER + "_"
            self.grid[-1][i] = SCREEN_BORDER + "_"
            self.grid[UPPER_WALL][i] = SCREEN_BORDER + "_"

        for i in range(SCREEN_ROWS):
            self.grid[i][0] = SCREEN_BORDER + "|"
            self.grid[i][-1] = SCREEN_BORDER + "|"

        self.grid[0][0] = self.grid[0][-1] = SCREEN_BORDER + " "

        # Printing Score and Lives
        self.grid[2], self.grid[3] = self.get_score_grid()

        # Printing Paddle
        paddle_left = self.paddle.x - self.paddle.length // 2
        paddle_right = self.paddle.x + self.paddle.length // 2
        for i in range(paddle_left, paddle_right + 1):
            self.grid[self.paddle.y][i] = PADDLE_COLOR + PAD_CHAR
        if self.paddle.is_shooter:
            self.grid[self.paddle.y - 1][paddle_left] = SHOOTING_PADDLE_AUG + PADDLE_COLOR
            self.grid[self.paddle.y - 1][paddle_right] = SHOOTING_PADDLE_AUG + PADDLE_COLOR

        # Printing Bullets
        for bullet in self.bullets:
            self.grid[round(bullet.y)][round(bullet.x)] = BULLET_COLOR + BULLET_CHAR

        # Printing bombs in boss level
        for bomb in self.bombs:
            self.grid[round(bomb.y)][round(bomb.x)] = BOMB_COLOR + BOMB_CHAR

        # Printing boss of boss level
        if self.level == BOSS_LEVEL:
            boss_x = round(self.boss.x)
            for x in range(boss_x - BOSS_WIDTH // 2, boss_x + BOSS_WIDTH // 2 + 1):
                for y in range(self.boss.y - BOSS_HEIGHT // 2, self.boss.y + BOSS_HEIGHT // 2 + 1):
                    self.grid[round(y)][round(x)] = BOSS_COLOR + BOSS[y - (self.boss.y - BOSS_HEIGHT // 2)][
                        x - (boss_x - BOSS_WIDTH // 2)]

        # Printing Balls
        for ball in self.balls:
            if ball.is_fireball:
                self.grid[round(ball.y)][round(ball.x)] = FIRE_BALL_COLOR + BALL_CHAR
            else:
                self.grid[round(ball.y)][round(ball.x)] = BALL_COLOR + BALL_CHAR

        # Printing Bricks
        for brick in self.bricks:
            brick_left = brick.x - brick.length // 2
            brick_right = brick.x + brick.length // 2
            for i in range(brick_left, brick_right + 1):
                self.grid[brick.y][i] = brick.color + brick.char
            self.grid[brick.y][brick_left] = brick.color + "["
            self.grid[brick.y][brick_right] = brick.color + "]"

        # Printing Powers
        for power in self.visible_powers:
            self.grid[round(power.y)][round(power.x)] = power.color + power.char

    def print_grid(self):
        print("\x1b[{}A".format(SCREEN_ROWS + 1))
        for row in self.grid:
            for el in row:
                print(el, end="")
            print(Style.RESET_ALL)

    def get_score_grid(self):
        tim = int(time() - self.start_time)

        score_line = [SCREEN_BORDER + "|"]
        if self.level != BOSS_LEVEL:
            score_str = "  SCORE = {}   TIME = {}   LIVES = {}   LEVEL = {}  FALLING TIMEOUT = {}" \
                .format(self.score, tim, self.lives, self.level,
                        FALLING_BRICKS_TIMEOUT[self.level] - tim
                        if FALLING_BRICKS_TIMEOUT[self.level] - tim > 0 else "ACTIVATED")
        else:
            score_str = "  SCORE = {}   TIME = {}   LIVES = {}   LEVEL = BOSS  BOSS HEALTH = {}" \
                .format(self.score, tim, self.lives, "".join([BOSS_HEALTH_CHAR for _ in range(self.boss.strength)]))

        for i in range(SCREEN_COLS - 2 - len(score_str)):
            score_str += " "
        score_line.append(SCREEN_BG + score_str)
        score_line.append(SCREEN_BORDER + "|")

        power_line = [SCREEN_BORDER + "|"]
        power_str = "  POWERUPS = "
        for tim, power in self.active_powers:
            power_str += ("{}({}) ".format(power.__class__.__name__, POWER_TIMEOUT - int(time() - tim)))
        for i in range(SCREEN_COLS - 2 - len(power_str)):
            power_str += " "
        power_line.append(DATA_COLOR + power_str)
        power_line.append(SCREEN_BORDER + "|")

        return score_line, power_line

    @staticmethod
    def run_game():
        score = None
        tim = None
        try:
            print("\n")
            print("Easy Mode: Velocity of ball is capped")
            print("Difficult Mode: Velocity of ball is uncapped")
            print("Press e for Easy and anything else for difficult and ENTER")
            inp = input("Difficulty Level: ")
            if inp == "e":
                mode = "Easy"
            else:
                mode = "Difficult"
            init()
            game = Game(mode)
            clear_screen()
            score, tim = game.start()

        finally:
            fd = sys.stdin.fileno()
            settings = termios.tcgetattr(fd)
            settings[3] = settings[3] | termios.ECHO
            termios.tcsetattr(fd, termios.TCSADRAIN, settings)
            print(Style.RESET_ALL)
            deinit()
            if score is not None and tim is not None:
                play_music("GameOver")
                print("\n\n\n\n\n\n")
                print("\t\tTotal Score = {}".format(score))
                print("\t\tTotal Time = {}".format(tim))
                print("\n\n\n\n\n\n")
