from colorama import Fore, Back

# Screen Info
SCREEN_BG = Back.WHITE
SCREEN_BORDER = Back.BLACK + Fore.BLACK
DATA_COLOR = Back.WHITE + Fore.BLACK
SCREEN_ROWS = 40
SCREEN_COLS = 130
UPPER_WALL = 4

# Game Info
LIVES = 3
FRAME_RATE = 10
TIMEOUT = 1 / FRAME_RATE

# Ball Info
BALL_VEL = 1
BALL_COLOR = Back.WHITE + Fore.RED
BALL_CHAR = "O"
MAX_BALL_STRENGTH = 10000

# Paddle Info
OFFSET_INCREASE = 1
PAD_LEN = 7
PAD_LEN_EXTENSION = 4
PAD_LEN_SHRINK = 4
PAD_CHAR = "T"
PAD_VEL = 1
PADDLE_COLOR = Back.GREEN + Fore.GREEN

# Brick Info
BRICK_LEN = 5
BRICK_CHAR = ["@", "#", "&", "+", "%"]
BRICK_COLOR = [Back.GREEN + Fore.GREEN,
               Back.BLUE + Fore.BLUE,
               Back.RED + Fore.RED,
               Back.BLACK + Fore.BLACK,
               Back.YELLOW + Fore.YELLOW]

# Powers Info
POWER_VEL = 0.5
FAST_BALL_VEL = 1 * BALL_VEL
POWER_CHANCES = 3
POWER_TIMEOUT = 10
POWER_COLOR = {
    'ExpandPaddle': Back.RED + Fore.YELLOW,
    'ShrinkPaddle': Back.RED + Fore.YELLOW,
    'BallMultiplier': Back.RED + Fore.YELLOW,
    'FastBall': Back.RED + Fore.YELLOW,
    'ThruBall': Back.RED + Fore.YELLOW,
    'PaddleGrab': Back.RED + Fore.YELLOW
}