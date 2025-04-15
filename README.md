# Connect Four Game with AI

A web-based implementation of the classic Connect Four game that demonstrates different AI algorithms using the minimax algorithm with various optimization techniques.

## Overview

This Connect Four implementation allows you to play against an AI that uses different strategies:

- **Plain Evaluation Function**: Basic minimax algorithm with a simple heuristic evaluation
- **Fail-Soft Alpha-Beta Pruning**: Optimized minimax with fail-soft alpha-beta pruning
- **Fail-Hard Alpha-Beta Pruning**: Optimized minimax with fail-hard alpha-beta pruning

## Features

- Clean web interface with a responsive game board
- Multiple AI difficulty levels through different algorithm implementations
- Easy switching between game modes
- Visual indication of game state (winning, tie)

## Technical Details

### Project Structure

```
connect-four/
├── app.py                # Flask application entry point
├── games/
│   ├── plain_eval.py     # Basic minimax implementation
│   ├── fail_soft.py      # Fail-soft alpha-beta pruning implementation
│   └── fail_hard.py      # Fail-hard alpha-beta pruning implementation
├── templates/
│   └── index.html        # Game interface
├── .gitignore            # Git ignore file
└── README.md             # This file
```

### Algorithms

#### Plain Evaluation Function

The basic minimax algorithm explores the game tree to a specified depth, evaluating board positions using a heuristic function that considers:
- Potential two-in-a-row and three-in-a-row sequences
- Completed four-in-a-row sequences

#### Alpha-Beta Pruning

Both fail-soft and fail-hard alpha-beta pruning implementations optimize the minimax algorithm by pruning branches that cannot influence the final decision, significantly reducing the search space.

The key differences between the implementations:
- **Fail-Soft**: Returns the actual minimax value even when pruning occurs
- **Fail-Hard**: Returns a bound (alpha or beta) when pruning occurs

### Game Evaluation

The heuristic evaluation function analyzes the board by:
1. Counting potential winning sequences for both players
2. Assigning higher values to more favorable positions (e.g., three-in-a-row is worth more than two-in-a-row)
3. Considering opponent's threats when calculating the score

## Demo
[[Watch a Demo!]](https://www.loom.com/share/eafacac748094f6badc13372ca73e13e?sid=b5b86410-36c1-4be8-ace5-13f9595f8a41)

## Getting Started

### Prerequisites

- Python 3.6+
- Flask

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/connect-four.git
cd connect-four
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required dependencies:
```bash
pip install flask
```

### Running the Game

1. Start the Flask application:
```bash
flask --app app.py --debug run
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

3. Select a game mode from the dropdown menu and start playing!

## How to Play

1. Choose a game mode from the dropdown menu.
2. Click on a column to drop your piece (yellow).
3. The AI (red) will automatically make its move.
4. The first player to connect four pieces horizontally, vertically, or diagonally wins.


## Acknowledgments

- The minimax algorithm and alpha-beta pruning implementations are based on classic AI game theory concepts.
- The web interface uses Flask for server-side rendering.