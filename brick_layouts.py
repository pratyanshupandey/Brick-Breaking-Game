from brick import *


def load_layout(layout):
    if layout == BOSS_LEVEL:
        return []
    if layout == 1:
        return brick_layout1()
    elif layout == 2:
        return brick_layout2()
    elif layout == 3:
        return brick_layout3()
    else:
        return []


def brick_layout1():
    bricks = []
    for i in range(15, 100, BRICK_LEN):
        bricks.append(RainbowBrick(i, 14))
    j = 0
    for i in range(15, 100, BRICK_LEN):
        j += 1
        if j % 3 == 0:
            bricks.append(OneHitBrick(i, 13))
        elif j % 3 == 1:
            bricks.append(TwoHitBrick(i, 13))
        else:
            bricks.append(ThreeHitBrick(i, 13))
    return bricks


def brick_layout2():
    bricks = []
    for i in range(15, 100, BRICK_LEN):
        bricks.append(ExplodingBrick(i, 13))

    j = 0
    for i in range(15, 100, BRICK_LEN):
        j += 1
        if j % 4 == 0:
            bricks.append(OneHitBrick(i, 14))
        elif j % 4 == 1:
            bricks.append(TwoHitBrick(i, 14))
        elif j % 4 == 2:
            bricks.append(ThreeHitBrick(i, 14))
        else:
            bricks.append(UnbreakableBrick(i, 14))

    bricks.append(OneHitBrick(62, 16))
    return bricks


def brick_layout3():
    bricks = []
    for i in range(25, 100, BRICK_LEN):
        bricks.append(OneHitBrick(i, 15))
    for i in range(25, 100, BRICK_LEN):
        bricks.append(TwoHitBrick(i, 14))
    for i in range(25, 100, BRICK_LEN):
        bricks.append(ExplodingBrick(i, 13))
    for i in range(25, 100, BRICK_LEN):
        bricks.append(UnbreakableBrick(i, 12))
    return bricks


def boss_brick_1():
    bricks = []
    for i in range(1 + BRICK_LEN//2, SCREEN_COLS - SCREEN_COLS % BRICK_LEN, BRICK_LEN):
        bricks.append(OneHitBrick(i, BOMB_Y + 1))
    return bricks


def boss_brick_2():
    bricks = []
    for i in range(1 + BRICK_LEN//2, SCREEN_COLS - SCREEN_COLS % BRICK_LEN, BRICK_LEN):
        bricks.append(TwoHitBrick(i, BOMB_Y + 2))
    return bricks
