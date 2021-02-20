# Terminal Game 

---
### Name: Pratyanshu Pandey
### Roll Number: 2019101025

---
### Instructions to run the game

Type the following in your bash terminal from the root directory of the game.

```bash
pip3 install -r requirements.txt
python3 game.py
```

### About the Game
The game is like a classic Ball Brick game just implemented on a terminal. The game starts with a paddle with a ball 
resting on it at some random position on the paddle. Press `x` to launch the ball. The direction and velocity of the ball will depend
on how farther it was placed from the centre of the paddle. The farther the ball the higher the x velocity in that direction.
When the ball collides with a brick, it reduces the strength of the brick by 1. When the strength of the brick becomes 0 it breaks
and there is 1 in 3 chance that a powerup is released. The objective of the game is to break all the breakable bricks and if possible the unbreakable
bricks too using explosion of Exploding Bricks.

#### Bricks:

| Type of Bricks | Break Score | Symbol | Color |
|:--------------:|:-----------:|:------:|:-----:|
| One Hit Brick  | 10 | @ | <span style="color:green">Green</span> |
| Two Hit Brick  | 30 | # | <span style="color:blue">Blue</span> |
| Three Hit Brick  | 100 | & | <span style="color:red">Red</span> |
| Unbreakable Brick  | 200 | + | Black |
| Exploding Brick  | 30 | % | <span style="color:#d1c406">Yellow</span> |

#### Power Up:

| Type of Power Ups | Symbol | Color | Description |
|:--------------:|:------:|:-----:|:---|
| Expand Paddle  |@ | <span style="color:green">Green</span> | Increase paddle size by 4 units | 
| Shrink Paddle  |# | <span style="color:red">Red</span> | Decrease paddle size by 4 units |
| Ball Multiplier  | & | <span style="color:blue">Blue</span> | Each ball divides into 2 with some x velocity |
| Fast Ball  | + | <span style="color:black">Black</span> | Increase vertical speed of all balls by 1 unit |
| Thru Ball  | % | <span style="color:cyan">Cyan</span> | Ball can go through bricks even unbreakable ones |
| Paddle Grab  | % | <span style="color:magenta">Magenta</span> | Ball can now stick to the paddle. Press `x` to release the ball |



### Game Moves
* `a` for moving the paddle left
* `d` for moving the paddle right
* `x` for launching the ball

### Start the Game
* Revise the possible moves from the instructions given
* Enter `p` and press `ENTER` to start playing the game
* Enter `q` and press `ENTER` to start exit the game


