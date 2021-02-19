from screen import run_game

start_screen = "Hello"
print(start_screen)

while True:

    val = input("Enter q for exit and p for play: ")
    if val == 'p':
        run_game()
    elif val == 'q':
        break
    else:
        print("Invalid Input")
