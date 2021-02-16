from time import sleep
from config import *
from paddle import Paddle
from ball import Ball
from utils import *
from input import get_input
from time import time
from brick_layouts import *
from powerup import *


class Game:
    def __init__(self, bricks):
        self.paddle = Paddle()
        self.balls = [Ball()]
        self.visible_powers = []
        self.active_powers = []
        self.bricks = bricks
        self.grid = []
        self.is_running = True
        self.lives = 3
        self.score = 0
        self.last_loaded = time()
        self.start_time = time()

    def loop(self):
        # i = 0
        while self.is_running:
            # sleep(0.1)
            inp = get_input()
            if inp == "a" or inp == "d":
                self.paddle.move(inp)
            elif inp == "x":
                for ball in self.balls:
                    ball.launch()
            elif inp == "q":
                break
            else:
                pass

            add_score, new_powers = ball_brick_collision(self.balls, self.bricks)
            self.score += add_score
            for power in new_powers:
                self.visible_powers.append(power)

            for ball in self.balls:
                if not ball.move(self.paddle):
                    self.balls.remove(ball)

            for power in self.visible_powers:
                val = power.move(self.paddle)
                if val == 1:
                    if isinstance(power, BallMultiplier):
                        self.balls = power.power(self.paddle, self.balls)
                    elif power.power(self.paddle, self.balls):
                        self.active_powers.append((time(), power))
                    self.visible_powers.remove(power)
                elif val == -1:
                    self.visible_powers.remove(power)
                else:
                    pass

            for start_time, power in self.active_powers:
                if time()-start_time >= POWER_TIMEOUT:
                    power.unpower(self.paddle, self.balls)
                    self.active_powers.remove((start_time,power))

            if len(self.balls) == 0 or len(self.bricks) == 0:
                self.is_running = False

            # print(inp)
            self.create_grid()
            while time() - self.last_loaded < TIMEOUT:
                pass
            self.print_grid()

    def create_grid(self):
        self.grid = []
        for i in range(SCREEN_ROWS):
            self.grid.append([])
            for j in range(SCREEN_COLS):
                self.grid[i].append(" ")

        # Screen Box
        for i in range(SCREEN_COLS):
            self.grid[0][i] = "_"
            self.grid[-1][i] = "_"
            self.grid[UPPER_WALL][i] = "_"

        for i in range(SCREEN_ROWS):
            self.grid[i][0] = "|"
            self.grid[i][-1] = "|"

        self.grid[0][0] = self.grid[0][-1] = " "

        # Printing Score and Lives
        self.grid[2] = "|\tSCORE = {} \t \t TIME = {} \t \t LIVES = {}".format(self.score, int(time() - self.start_time), self.lives)
        self.grid[3] = "|\tPOWERUPS = "
        for tim, power in self.active_powers:
            self.grid[3] += "{}({}) ".format( power.__class__.__name__ ,POWER_TIMEOUT - int(time() - tim))

        # Printing Paddle
        paddle_left = self.paddle.x - self.paddle.length // 2
        paddle_right = self.paddle.x + self.paddle.length // 2
        for i in range(paddle_left, paddle_right + 1):
            self.grid[self.paddle.y][i] = PAD_CHAR

        # Printing Balls
        for ball in self.balls:
            file = open("demofile3.txt", "a")
            file.write("{} {} {} {}\n".format(ball.x, ball.y, ball.x_velocity, ball.y_velocity))
            file.close()
            self.grid[ball.y][ball.x] = "O"

        # Printing Bricks
        for brick in self.bricks:
            brick_left = brick.x - brick.length // 2
            brick_right = brick.x + brick.length // 2
            for i in range(brick_left, brick_right + 1):
                self.grid[brick.y][i] = brick.char

        # Printing Powers
        for power in self.visible_powers:
            self.grid[power.y][power.x] = power.char

    def print_grid(self):
        print("\x1b[{}A".format(SCREEN_ROWS + 1))
        for row in self.grid:
            for el in row:
                print(el, end="")
            print()
        self.last_loaded = time()


brick_layout = brick_layout1()
game = Game(brick_layout)
clear_screen()
game.loop()
