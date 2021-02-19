from brick import *


def brick_layout1():
    bricks = []
    for i in range(8,120,5):
        bricks.append(OneHitBrick(i, 14))
    for i in range(8,120,5):
        bricks.append(TwoHitBrick(i, 13))
    for i in range(8,120,5):
        bricks.append(ThreeHitBrick(i, 12))
    for i in range(8,120,5):
        bricks.append(UnbreakableBrick(i, 11))
    for i in range(8,120,5):
        bricks.append(ExplodingBrick(i, 10))
    return bricks
