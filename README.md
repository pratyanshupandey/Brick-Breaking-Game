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
The game is like a classic Ball Brick game just implemented on a terminal. The objective of the game is to destroy all
breakable bricks by directing the ball with the paddle to collide with these bricks.
Destroying unbreakable bricks gives a bonus.

#### Gameplay and Rules

* The game starts with a paddle with a ball resting on it at some random position on the paddle. 
* Press `x` to launch the ball. The direction and velocity of the ball will depend on how farther it was placed from the 
  centre of the paddle. The farther the ball the higher the x velocity in that direction.
* When the ball collides with a brick, it reduces the strength of the brick by 1. 
* When the strength of the brick becomes 0 it breaks and there is 1 in 3 chance that a powerup is released.
* One can catch a powerup using the paddle. A powerup remains active for 10 seconds. Powerups can be stacked together.
* When the ball collides with the borders of the screens, it is reflected back.
* When a ball misses the paddle and collides with the bottom wall a life is lost and everything other than the brick 
  layout is reset. 
* You have 3 lives to finish the game.
* You can see your current score, time taken, lives remaining and active powerups on the top panel.

#### Collision of ball and paddle
When the ball collides with the paddle, the vertical velocity is reflected. A number is added to the horizontal velocity 
depending upon how far the collision point was from centre of the paddle. This number is positive for collision on right 
side of the paddle and negative for the left side of the paddle.

#### Bricks:

| Type of Bricks | Break Score | Symbol | Color | Description |
|:--------------:|:-----------:|:------:|:-----:|:-----------:|
| One Hit Brick  | 10 | @ | <span style="color:green">Green</span> | Get destroyed in 1 hit |
| Two Hit Brick  | 30 | # | <span style="color:blue">Blue</span> | Get destroyed in 2 hit |
| Three Hit Brick  | 100 | & | <span style="color:red">Red</span> | Get destroyed in 3 hit |
| Unbreakable Brick  | 200 | + | Black | Can only be destroyed through explosion or ThruBall |
| Exploding Brick  | 30 | % | <span style="color:#d1c406">Yellow</span> | Get destroyed in 1 hit and also destroys every brick adjacent to it |

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
* Enter `q` and press `ENTER` to exit the game
* Enter `p` and press `ENTER` to start playing the game
* Choose a layout and press `ENTER`

