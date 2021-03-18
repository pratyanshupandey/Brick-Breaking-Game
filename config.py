from colorama import Fore, Back, Style

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
OFFSET_INCREASE = 0.5
PAD_VEL = 2
PAD_VER_OFF = 4
PAD_LEN = 11
PAD_LEN_EXTENSION = 4
PAD_LEN_SHRINK = 4
PAD_CHAR = "T"
PADDLE_COLOR = Back.GREEN + Fore.RED + Style.DIM
SHOOTING_PADDLE_AUG = "|"

# Brick Info
FALLING_BRICKS_TIMEOUT = [50,50,50,50]
BRICK_LEN = 7
BRICK_STRENGTH = [1,2,3,MAX_BALL_STRENGTH - 1, 1]
BRICK_BREAK_SCORE = [10,30,100,200,30]
BRICK_CHAR = ["@", "#", "&", "+", "%"]
BRICK_COLOR = [Back.GREEN + Fore.GREEN + Style.DIM,
               Back.BLUE + Fore.BLUE + Style.DIM,
               Back.RED + Fore.RED + Style.DIM,
               Back.BLACK + Fore.BLACK + Style.DIM,
               Back.YELLOW + Fore.YELLOW + Style.DIM]

# Powers Info
POWER_VEL = 0.5
FAST_BALL_VEL = 1 * BALL_VEL
POWER_CHANCES = 3
POWER_TIMEOUT = 10
POWER_COLOR = {
    'ExpandPaddle': Back.GREEN + Fore.YELLOW,
    'ShrinkPaddle': Back.RED + Fore.YELLOW,
    'BallMultiplier': Back.BLUE + Fore.YELLOW,
    'FastBall': Back.BLACK + Fore.YELLOW,
    'ThruBall': Back.CYAN + Fore.YELLOW,
    'PaddleGrab': Back.MAGENTA + Fore.YELLOW,
    'ShootingPaddle': Back.WHITE + Fore.YELLOW
}
GRAVITY = -1

# Bullets Info
BULLET_CHAR = "I"
BULLET_COLOR = Back.WHITE + Fore.BLACK
BULLET_SPEED = -1
BULLET_TIMEOUT = 1