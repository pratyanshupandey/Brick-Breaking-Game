from brick import *


def brick_layout1():
    bricks = []
    # for i in range(8,120,BRICK_LEN):
    #     bricks.append(OneHitBrick(i, 14))
    # for i in range(8,120,BRICK_LEN):
    #     bricks.append(TwoHitBrick(i, 13))
    # for i in range(8, 120, BRICK_LEN):
    #     bricks.append(ThreeHitBrick(i, 9))
    for i in range(8, 120, BRICK_LEN):
        bricks.append(UnbreakableBrick(i, 10))
    for i in range(8, 120, BRICK_LEN):
        bricks.append(ExplodingBrick(i, 11))
    return bricks
