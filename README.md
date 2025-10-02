# Boxoban MCP

A Python implementation of the Boxoban puzzle game with Model Context Protocol (MCP) support.

## Overview

Boxoban is a box-pushing puzzle game inspired by Sokoban. The aim is to push all boxes onto the target positions. Each level has four boxes and four targets. The player can push a box as long as nothing (another box or a wall) is behind it.

## Game Symbols

The game uses the following ASCII symbols:
- `#` - Wall
- `@` - Player character
- `$` - Box
- `.` - Goal/target position
- `*` - Box on a goal position
- `+` - Player on a goal position
- ` ` - Empty space

## Installation

This project uses `uv` as the package manager. To install the development dependencies:

```bash
uv pip install -e ".[dev]"
```

## Usage

### Loading a Game

There are three ways to load a Boxoban puzzle:

1. **From a string:**
```python
from src.boxoban_mcp.game import BoxobanGame

puzzle_string = """
##########
#     @  #
#  $ $.  #
#    $.  #
##########
"""
game = BoxobanGame.from_string(puzzle_string)
```

2. **From a file:**
```python
game = BoxobanGame.from_file('puzzles/hard/000.txt')
```

3. **Using dataset parameters:**
```python
# Load puzzle 12 from medium/train/001.txt
game = BoxobanGame.from_parameters('medium', 'train', '001', 12)

# Load puzzle 0 from hard/000.txt
game = BoxobanGame.from_parameters('hard', None, '000', 0)
```

### Playing the Game

```python
from src.boxoban_mcp.game import BoxobanGame, Direction

# Create a game
game = BoxobanGame.from_string(puzzle_string)

# Get valid moves
valid_moves = game.valid_moves()
print(f"Valid moves: {[move.name for move in valid_moves]}")

# Take an action
success = game.take_action(Direction.LEFT)
if success:
    print("Move successful!")
else:
    print("Invalid move!")

# Get current game state
state = game.get_state()
print(game)  # Print the current state

# Check if solved
if game.is_solved():
    print("Puzzle solved!")
```

### Direction Enum

The `Direction` enum provides four movement options:
- `Direction.UP` - Move up
- `Direction.DOWN` - Move down
- `Direction.LEFT` - Move left
- `Direction.RIGHT` - Move right

### Key Methods

- `valid_moves()` - Returns a list of valid `Direction` enums from the current position
- `take_action(direction)` - Attempts to move in the specified direction. Returns `True` if successful, `False` if invalid
- `get_state()` - Returns the current game state as a 2D list of strings
- `is_solved()` - Returns `True` if all boxes are on goal positions
- `copy()` - Creates a deep copy of the game state

## Running Tests

To run the test suite:

```bash
uv run pytest
```

To run with coverage:

```bash
uv run pytest --cov=src/boxoban_mcp
```

## Dataset Structure

The repository contains Boxoban puzzles organized by difficulty:

- **unfiltered/** - Contains train (900,000 puzzles), valid (100,000 puzzles), and test (1,000 puzzles)
- **medium/** - Contains train (450,000 puzzles) and valid (50,000 puzzles)
- **hard/** - Contains 3,332 puzzles

Each puzzle file contains multiple puzzles separated by semicolons and puzzle numbers. Each puzzle is a 10x10 grid.

## Citation

If you use this dataset in your work, please cite:

```bibtex
@misc{boxobanlevels,
author = {Arthur Guez and Mehdi Mirza and Karol Gregor and Rishabh Kabra and Sebastien Racaniere and Theophane Weber and David Raposo and Adam Santoro and Laurent Orseau and Tom Eccles and Greg Wayne and David Silver and Timothy Lillicrap and Victor Valdes},
title = {An investigation of Model-free planning: boxoban levels},
howpublished= {https://github.com/deepmind/boxoban-levels/},
year = "2018"
}
```

## License

This is not an official Google product.