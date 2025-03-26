# About the Game
This is a simulation of a two-player game where Player 1 (`drone.png`) can terminate the game anytime it wants and Player 2 (`robot.png`) can be either a cooperative or a competitive agent. Player 1 must terminate the game if it suspects defection from Player 2. But terminating the game when Player 2 is cooperative results in punishment for both. A cooperative agent would want to reach green cells in the grid world and provide reward for all players, whereas a competitive agent would want to reach red cells to get a profit for itself and loss for others.

# About the Code
`simulation.py` runs the game simulation.
- specify grid world environment details in `environment.py`
- specify player details in `players.py`

`render.py` visualizes the game trajectory.
- specify the episode number to visualize in the variable `episode_number`
- make sure to have the `pygames` library

## Python Version
The code was written using `Python 3.9`. Any version of Python after `3.0` should be compatible.

## Installation and Running.
No installation required. Specify environment and player details in `environment.py` and `players.py` respectively. Run `simulation.py` to train the players. Enter which episode to visualize in `episode_number` in `render.py`. Run `render.py` to watch the game. Press SPACEBAR to go to the next turn.

## Required Libraries
The code uses the following Python packages:
- `json`
- `pygame`
- `random`

# Acknowledgment
TBD

# Contact Information
md.shuvo@ufl.edu

