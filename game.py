from screen import *

while True:

    print("\nIN GAME INSTRUCTIONS")
    print("a for moving paddle left")
    print("d for moving paddle right")
    print("x for launching the ball")
    print("READ THE README BEFORE FOR MORE DETAILS\n\n")

    print("START INSTRUCTIONS")
    print("p for starting the game")
    print("q for exiting the game")

    val = input("Option: ")
    if val == 'p':
        print("\n\n\nBrick Layouts")
        print("1. Without any Exploding Bricks")
        print("2. With Exploding Bricks")
        layout = input("Choose Layout: ")
        if layout.isnumeric() and int(layout) in range(1,3):
            Game.run_game(int(layout))
        else:
            print("Invalid Input")

    elif val == 'q':
        break
    else:
        print("Invalid Input")
