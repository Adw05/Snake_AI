# Snake Game AI (Deep Reinforcement Learning)

## Overview
This project is a classic **Snake** game built with **Pygame**, paired with a **Deep Reinforcement Learning** agent that learns to play the game by itself.

The AI is trained using a **Deep Q-Network (DQN)** implemented in **PyTorch**. During training, the agent plays many games, collects experience (state, action, reward, next state), and improves its decision-making over time.

## What you can do
- **Play (watch the AI)** run a Snake game using a pre-trained model.
- **Train your own model** and save it once a target performance is reached.
- **Visualize training progress** (score and mean score over games).

## Tech stack
- **Python**
- **Pygame**: game window, rendering, and real-time loop
- **PyTorch**: neural network (DQN), training, and GPU support (if available)
- **NumPy**: state vector / numeric operations
- **Matplotlib + IPython display**: live training plot

## How it works (simple explanation)
### Environment (the game)
The environment is implemented in `rl/environment.py`.

- The Snake moves on a **600x600** grid.
- Each move advances by **20 pixels** (grid-based movement).
- The game ends if the Snake hits:
  - a wall, or
  - its own body.

### State (what the AI “sees”)
The agent receives a **14-value state vector** (`state_size=14`) containing:
- Danger checks (collision ahead / right / left)
- Wall checks (wall ahead / right / left)
- Current movement direction (left/right/up/down)
- Food location relative to the head (food left/right/up/down)

### Actions (what the AI can do)
The action space is **3 actions** (`action_size=3`):
- `0`: go straight
- `1`: turn right
- `2`: turn left

These are **relative** actions based on the Snake’s current heading.

### Rewards (how learning is guided)
- **+10** for eating food
- **-10** for dying (collision)
- A small **time penalty** each step to encourage efficient paths

### Learning algorithm
The agent in `rl/agent.py` uses:
- **DQN** (a small fully-connected network)
- **Experience replay** (a memory buffer)
- **Epsilon-greedy exploration** (random moves early, more greedy later)
- A **target network** to stabilize learning (updated periodically)

## Project structure
```
Snake_Game_AI/
  components/         # Game objects (snake, food, scoreboard)
  model/              # Saved model weights (.pth)
  rl/                 # RL agent + environment
  script/             # Entry points (train/play) + training plot image
```

## Setup
### 1) Create and activate a virtual environment (recommended)
```bash
python -m venv .venv
```

Windows (PowerShell):
```powershell
.\.venv\Scripts\Activate.ps1
```

### 2) Install dependencies
```bash
pip install pygame torch numpy matplotlib ipython
```

Note: Installing PyTorch can vary by system (CPU vs CUDA). If you have issues, follow the official PyTorch install instructions for your machine.

## Run the project
Because the scripts use relative file paths for loading/saving models, **your working directory matters**.

### Watch the AI play (pre-trained)
- **Working directory**: `Snake_Game_AI/script`
- Run:
```bash
python play.py
```

This loads the pre-trained model file `model/smart_modelv2.pth`.

### Train a model
- **Working directory**: `Snake_Game_AI`
- Run:
```bash
python script/train.py
```

Training will:
- run without rendering for speed (`render_mode = False`)
- update a live plot and save it as `training_plot.png`
- save the model once the mean score reaches the target (see `script/train.py`)

## Notes / troubleshooting
- If imports like `snake_game.Snake_Game_AI...` fail in the terminal, run from your IDE (PyCharm) with the project root configured, or make sure the parent folder that contains `snake_game/` is on your `PYTHONPATH`.
- Close the Pygame window to exit.

