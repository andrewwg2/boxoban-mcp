# Boxoban MCP

A Python implementation of the Boxoban puzzle game with move validation and game state management.

## Overview

Boxoban is a box-pushing puzzle game inspired by Sokoban. The aim is to push boxes onto target positions. Each level has four boxes and four targets. The player can push a box as long as nothing (another box, a wall) is behind it.

## Installation

This project uses `uv` as the package manager. To install dependencies:

```bash
# Install the package with test dependencies
uv pip install -e ".[test]"
```

## Game Symbols

The game uses the following ASCII symbols:

- `#` - Wall
- `@` - Player
- `$` - Box
- `.` - Target/destination
- `*` - Box on target (box placed on a destination)
- `+` - Player on target (player standing on a destination)
- ` ` - Empty space

## Usage

### Loading a Game

The `Boxoban` class provides multiple ways to load a puzzle:

#### From String

```python
from src.boxoban_mcp import Boxoban

game_string = """##########
#   @    #
#   $    #
#   .    #
##########"""

game = Boxoban.from_string(game_string)
```

#### From File

```python
# Load the first puzzle from a file
game = Boxoban.from_file("puzzles/medium/valid/000.txt")
```

#### From Puzzle Directory Structure

```python
# Load a specific puzzle by its location in the directory structure
# Parameters: difficulty, dataset, file_num, puzzle_num
game = Boxoban.from_puzzle_path("medium", "train", "001", 12)
```

### Playing the Game

#### Check Valid Moves

```python
# Get list of valid moves from current position
valid_moves = game.valid_moves()
# Returns: ['up', 'down', 'left', 'right'] (only valid directions)
```

#### Take an Action

```python
# Attempt to move in a direction
success = game.take_action('left')
# Returns: True if move was legal and executed, False otherwise
```

#### Get Game State

```python
# Get the current game state as a string
state = game.get_state()
print(state)
```

#### Check if Solved

```python
# Check if all boxes are on targets
if game.is_solved():
    print("Puzzle solved!")
```

### Movement Rules

1. The player (`@`) can move in four directions: up, down, left, right
2. The player cannot move into walls (`#`)
3. The player can push boxes (`$`) if:
   - There's an empty space or target behind the box
   - There's no wall or another box behind it
4. When a box is pushed onto a target (`.`), it becomes `*`
5. When the player stands on a target, it becomes `+`
6. Targets are restored when boxes/player move away

### Example

```python
from src.boxoban_mcp import Boxoban

# Create a simple puzzle
game = Boxoban.from_puzzle_path("medium", "valid", "000", 0)

# Play the game
print("Initial state:")
print(game.get_state())
print(f"Valid moves: {game.valid_moves()}")

# Make a move
if game.take_action('down'):
    print("\nAfter moving down:")
    print(game.get_state())

# Check if solved
if game.is_solved():
    print("Congratulations! Puzzle solved!")
```

## Running Tests

Run the test suite using pytest:

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/test_boxoban.py
```

## Puzzle Files

Puzzles are organized in the following structure:
- `puzzles/unfiltered/` - Contains train (900,000), valid (100,000), and test (1,000) puzzles
- `puzzles/medium/` - Contains train (450,000) and valid (50,000) puzzles
- `puzzles/hard/` - Contains 3,332 puzzles

Each file contains multiple puzzles separated by semicolons and puzzle numbers.

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