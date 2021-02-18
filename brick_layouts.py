from brick import *


def brick_layout1():
    bricks = []
    # return bricks
    for i in range(8,120,5):
        bricks.append(OneHitBrick(i, 18))
    for i in range(8,120,5):
        bricks.append(TwoHitBrick(i, 17))
    # bricks = []
    return bricks
