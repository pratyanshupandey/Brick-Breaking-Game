from paddle import Paddle
from ball import Ball
from point import *
from input import get_input
from time import time
from brick_layouts import *
from powerup import *
import termios
import sys
from colorama import init, deinit, Style


class Game:
    def __init__(self):
        self.paddle = Paddle()
        self.balls = [Ball()]
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
        while self.lives > 0 and self.level < 4:
            # -1 quitgame
            # 0 all bricks done
            # 1 no ball left
            # 2 next level skip
            val = self.loop()
            if val == -1:
                break
            elif val == 0 or val == 2:
                self.level += 1
                self.bricks = load_layout(self.level)
            elif val == 1:
                self.lives -= 1

            self.balls = [Ball()]
            self.visible_powers = []
            self.active_powers = []
            self.paddle = Paddle()

        return self.score, int(time() - self.start_time)

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

            # Moving Balls, Checking Collisions and Creating Powers
            for ball in self.balls:
                is_ball, add_score, new_powers, paddle_col = ball.move(self.paddle, self.bricks)
                if not is_ball:
                    self.balls.remove(ball)
                self.score += add_score
                for power in new_powers:
                    self.visible_powers.append(power)

            # Managing Powers
            for power in self.visible_powers:
                val = power.move(self.paddle)
                if val == 1:
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
                    else:
                        self.bricks[i] = self.bricks[i].replace()

            for start_time, power in self.active_powers:
                if time() - start_time >= POWER_TIMEOUT:
                    power.unpower(self.paddle, self.balls)
                    self.active_powers.remove((start_time, power))

            if Brick.br_count(self.bricks) == 0:
                return 0
            elif len(self.balls) == 0:
                return 1

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
        self.grid[2], self.grid[3] = Game.get_score_grid(self.score, int(time() - self.start_time), self.lives,
                                                         self.active_powers, time())

        # Printing Paddle
        paddle_left = self.paddle.x - self.paddle.length // 2
        paddle_right = self.paddle.x + self.paddle.length // 2
        for i in range(paddle_left, paddle_right + 1):
            self.grid[self.paddle.y][i] = PADDLE_COLOR + PAD_CHAR

        # Printing Balls
        for ball in self.balls:
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

    @staticmethod
    def get_score_grid(score, tim, lives, powers, cur_time):
        score_line = [SCREEN_BORDER + "|"]
        score_str = "  SCORE = {}   TIME = {}   LIVES = {}".format(score, tim, lives)
        for i in range(SCREEN_COLS - 2 - len(score_str)):
            score_str += " "
        score_line.append(SCREEN_BG + score_str)
        score_line.append(SCREEN_BORDER + "|")

        power_line = [SCREEN_BORDER + "|"]
        power_str = "  POWERUPS = "
        for tim, power in powers:
            power_str += ("{}({}) ".format(power.__class__.__name__, POWER_TIMEOUT - int(cur_time - tim)))
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
            init()
            game = Game()
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
                print("\n\n\n\n\n\n")
                print("\t\tTotal Score = {}".format(score))
                print("\t\tTotal Time = {}".format(tim))
                print("\n\n\n\n\n\n")
