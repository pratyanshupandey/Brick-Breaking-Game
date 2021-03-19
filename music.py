import os


def play_music(event):
    if event == "collision":
        os.system("aplay -q Sounds/POP.WAV > /dev/null &")
    elif event == "PowerupCatch":
        os.system("aplay -q Sounds/DING.WAV > /dev/null &")
    elif event == "GameOver":
        os.system("aplay -q Sounds/CHIMES.WAV > /dev/null &")
    elif event == "NewLevel":
        os.system("aplay -q Sounds/CHIMES.WAV > /dev/null &")
    elif event == "Explosion":
        os.system("aplay -q Sounds/EXPLODE.WAV > /dev/null &")
    elif event == "LifeLost":
        os.system("aplay -q Sounds/PARRAM.WAV > /dev/null &")
    else:
        pass
