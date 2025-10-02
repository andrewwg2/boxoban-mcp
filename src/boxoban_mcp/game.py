"""
Boxoban game implementation.

The game uses the following symbols:
- '#' for wall
- '@' for the player character
- '$' for a box
- '.' for a goal position
- '*' for a box on a goal position
- '+' for the player on a goal position
- ' ' for empty space
"""

from pathlib import Path
from typing import List, Tuple, Optional, Set
from enum import Enum
import copy


class Direction(Enum):
    """Enum for movement directions."""
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)


class BoxobanGame:
    """
    A class to represent and manipulate Boxoban puzzles.
    
    Attributes:
        grid: 2D list representing the game state
        player_pos: Tuple (row, col) of player position
        boxes: Set of tuples representing box positions
        goals: Set of tuples representing goal positions
    """
    
    # Symbol constants
    WALL = '#'
    PLAYER = '@'
    BOX = '$'
    GOAL = '.'
    BOX_ON_GOAL = '*'
    PLAYER_ON_GOAL = '+'
    EMPTY = ' '
    
    def __init__(self, grid: List[List[str]]):
        """Initialize the game with a grid."""
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0
        self._parse_grid()
    
    def _parse_grid(self):
        """Parse the grid to extract player position, boxes, and goals."""
        self.player_pos = None
        self.boxes = set()
        self.goals = set()
        
        for row in range(self.height):
            for col in range(self.width):
                cell = self.grid[row][col]
                
                if cell == self.PLAYER:
                    self.player_pos = (row, col)
                    self.grid[row][col] = self.EMPTY
                elif cell == self.PLAYER_ON_GOAL:
                    self.player_pos = (row, col)
                    self.goals.add((row, col))
                    self.grid[row][col] = self.EMPTY
                elif cell == self.BOX:
                    self.boxes.add((row, col))
                    self.grid[row][col] = self.EMPTY
                elif cell == self.BOX_ON_GOAL:
                    self.boxes.add((row, col))
                    self.goals.add((row, col))
                    self.grid[row][col] = self.EMPTY
                elif cell == self.GOAL:
                    self.goals.add((row, col))
                    self.grid[row][col] = self.EMPTY
                elif cell == self.WALL:
                    pass  # Keep walls as they are
                else:
                    self.grid[row][col] = self.EMPTY
    
    def get_state(self) -> List[List[str]]:
        """
        Return the current game state as a 2D grid with all symbols.
        
        Returns:
            2D list of strings representing the current game state
        """
        state = [row[:] for row in self.grid]  # Deep copy of grid
        
        # Add goals
        for row, col in self.goals:
            if state[row][col] == self.EMPTY:
                state[row][col] = self.GOAL
        
        # Add boxes
        for row, col in self.boxes:
            if (row, col) in self.goals:
                state[row][col] = self.BOX_ON_GOAL
            else:
                state[row][col] = self.BOX
        
        # Add player
        if self.player_pos:
            row, col = self.player_pos
            if (row, col) in self.goals:
                state[row][col] = self.PLAYER_ON_GOAL
            else:
                state[row][col] = self.PLAYER
        
        return state
    
    def valid_moves(self) -> List[Direction]:
        """
        Get list of valid moves from current position.
        
        A move is valid if:
        - The player doesn't hit a wall
        - If moving into a box, the box can be pushed (not into wall or another box)
        
        Returns:
            List of Direction enums representing valid moves
        """
        valid = []
        
        if not self.player_pos:
            return valid
        
        player_row, player_col = self.player_pos
        
        for direction in Direction:
            dr, dc = direction.value
            new_row = player_row + dr
            new_col = player_col + dc
            
            # Check bounds
            if not (0 <= new_row < self.height and 0 <= new_col < self.width):
                continue
            
            # Check if moving into wall
            if self.grid[new_row][new_col] == self.WALL:
                continue
            
            # Check if moving into box
            if (new_row, new_col) in self.boxes:
                # Check if box can be pushed
                box_new_row = new_row + dr
                box_new_col = new_col + dc
                
                # Check bounds for box
                if not (0 <= box_new_row < self.height and 0 <= box_new_col < self.width):
                    continue
                
                # Check if box would hit wall or another box
                if (self.grid[box_new_row][box_new_col] == self.WALL or 
                    (box_new_row, box_new_col) in self.boxes):
                    continue
            
            valid.append(direction)
        
        return valid
    
    def take_action(self, direction: Direction) -> bool:
        """
        Take an action in the specified direction.
        
        Args:
            direction: Direction enum indicating the movement direction
            
        Returns:
            True if the action was legal and executed, False otherwise
        """
        if direction not in self.valid_moves():
            return False
        
        dr, dc = direction.value
        player_row, player_col = self.player_pos
        new_row = player_row + dr
        new_col = player_col + dc
        
        # Check if pushing a box
        if (new_row, new_col) in self.boxes:
            box_new_row = new_row + dr
            box_new_col = new_col + dc
            
            # Move the box
            self.boxes.remove((new_row, new_col))
            self.boxes.add((box_new_row, box_new_col))
        
        # Move the player
        self.player_pos = (new_row, new_col)
        
        return True
    
    def is_solved(self) -> bool:
        """Check if the puzzle is solved (all boxes on goals)."""
        return self.boxes == self.goals
    
    def copy(self) -> 'BoxobanGame':
        """Create a deep copy of the game state."""
        new_game = BoxobanGame([row[:] for row in self.grid])
        new_game.player_pos = self.player_pos
        new_game.boxes = self.boxes.copy()
        new_game.goals = self.goals.copy()
        return new_game
    
    @classmethod
    def from_string(cls, puzzle_string: str) -> 'BoxobanGame':
        """
        Create a BoxobanGame instance from a puzzle string.
        
        Args:
            puzzle_string: String representation of the puzzle
            
        Returns:
            BoxobanGame instance
        """
        lines = puzzle_string.strip().split('\n')
        # Remove puzzle number line if present
        if lines and lines[0].startswith(';'):
            lines = lines[1:]
        
        # Filter out empty lines
        lines = [line for line in lines if line.strip()]
        
        # Convert to grid
        grid = [list(line) for line in lines]
        
        return cls(grid)
    
    @classmethod
    def from_file(cls, file_path: str) -> 'BoxobanGame':
        """
        Load a single puzzle from a file.
        
        Args:
            file_path: Path to the puzzle file
            
        Returns:
            BoxobanGame instance of the first puzzle in the file
        """
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Split by puzzle separator and get the first puzzle
        puzzles = content.split(';')
        if len(puzzles) > 1:
            # Skip the first empty part and get the first puzzle
            puzzle_text = ';' + puzzles[1].split(';')[0]
        else:
            puzzle_text = content
        
        return cls.from_string(puzzle_text)
    
    @classmethod
    def from_parameters(cls, difficulty: str, dataset: str, file_num: str, puzzle_num: int) -> 'BoxobanGame':
        """
        Load a specific puzzle using dataset parameters.
        
        Args:
            difficulty: 'hard', 'medium', or 'unfiltered'
            dataset: 'train', 'valid', or 'test' (not applicable for 'hard')
            file_num: File number (e.g., '001')
            puzzle_num: Puzzle number within the file
            
        Returns:
            BoxobanGame instance
            
        Example:
            game = BoxobanGame.from_parameters('medium', 'train', '001', 12)
        """
        # Construct file path
        if difficulty == 'hard':
            file_path = Path(f'puzzles/{difficulty}/{file_num}.txt')
        else:
            file_path = Path(f'puzzles/{difficulty}/{dataset}/{file_num}.txt')
        
        # Read the file
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Split by puzzle separator
        puzzles = content.split(f'; {puzzle_num}')
        if len(puzzles) < 2:
            raise ValueError(f"Puzzle number {puzzle_num} not found in file")
        
        # Get the puzzle text (everything until the next separator or end)
        puzzle_text = puzzles[1].split(';')[0]
        
        return cls.from_string(puzzle_text)
    
    def __str__(self) -> str:
        """String representation of the current game state."""
        state = self.get_state()
        return '\n'.join(''.join(row) for row in state)