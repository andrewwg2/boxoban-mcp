"""Boxoban game implementation."""

from typing import List, Tuple, Optional
from pathlib import Path
import copy


class Boxoban:
    """
    A class to represent and play the Boxoban puzzle game.
    
    Game symbols:
    - '#': Wall
    - '@': Player
    - '$': Box
    - '.': Target/destination
    - '*': Box on target (new symbol)
    - '+': Player on target (new symbol)
    - ' ': Empty space
    """
    
    # Game symbols
    WALL = '#'
    PLAYER = '@'
    BOX = '$'
    TARGET = '.'
    BOX_ON_TARGET = '*'
    PLAYER_ON_TARGET = '+'
    EMPTY = ' '
    
    # Movement directions
    MOVES = {
        'up': (-1, 0),
        'down': (1, 0),
        'left': (0, -1),
        'right': (0, 1)
    }
    
    def __init__(self, game_state: List[List[str]]):
        """
        Initialize the Boxoban game with a given state.
        
        Args:
            game_state: 2D list representing the game board
        """
        self.grid = copy.deepcopy(game_state)
        self.height = len(self.grid)
        self.width = len(self.grid[0]) if self.height > 0 else 0
        self._find_player()
        
    def _find_player(self) -> None:
        """Find the current position of the player."""
        for i in range(self.height):
            for j in range(self.width):
                if self.grid[i][j] in (self.PLAYER, self.PLAYER_ON_TARGET):
                    self.player_pos = (i, j)
                    return
        raise ValueError("No player found in the game state")
    
    @classmethod
    def from_string(cls, game_string: str) -> 'Boxoban':
        """
        Create a Boxoban instance from a string representation.
        
        Args:
            game_string: String representation of the game
            
        Returns:
            Boxoban instance
        """
        lines = game_string.strip().split('\n')
        # Filter out puzzle number lines and empty lines
        lines = [line for line in lines if line and not line.startswith(';')]
        
        # Pad lines to ensure consistent width
        max_width = max(len(line) for line in lines) if lines else 0
        grid = []
        for line in lines:
            row = list(line.ljust(max_width))
            grid.append(row)
            
        return cls(grid)
    
    @classmethod
    def from_file(cls, file_path: str) -> 'Boxoban':
        """
        Create a Boxoban instance from a file.
        
        Args:
            file_path: Path to the file containing the game
            
        Returns:
            Boxoban instance
        """
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Split by puzzle separator and get the first puzzle
        puzzles = content.split(';')
        if len(puzzles) > 1:
            # Skip the first empty split and get the actual first puzzle
            puzzle_content = puzzles[1].strip()
            # Remove the puzzle number line
            lines = puzzle_content.split('\n')
            if lines and lines[0].strip().isdigit():
                puzzle_content = '\n'.join(lines[1:])
        else:
            puzzle_content = content
            
        return cls.from_string(puzzle_content)
    
    @classmethod
    def from_puzzle_path(cls, difficulty: str, dataset: str, file_num: str, puzzle_num: int) -> 'Boxoban':
        """
        Create a Boxoban instance from the puzzle directory structure.
        
        Args:
            difficulty: 'medium', 'hard', or 'unfiltered'
            dataset: 'train', 'valid', or 'test'
            file_num: File number (e.g., '001')
            puzzle_num: Puzzle number within the file
            
        Returns:
            Boxoban instance
        """
        file_path = Path(f"./puzzles/{difficulty}/{dataset}/{file_num}.txt")
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        # Split by puzzle separator
        puzzles = content.split(';')
        
        # Find the puzzle with the requested number
        for i, puzzle in enumerate(puzzles):
            if not puzzle.strip():
                continue
                
            lines = puzzle.strip().split('\n')
            if lines and lines[0].strip() == str(puzzle_num):
                # Found the puzzle, remove the number line
                puzzle_content = '\n'.join(lines[1:])
                return cls.from_string(puzzle_content)
                
        raise ValueError(f"Puzzle {puzzle_num} not found in file {file_path}")
    
    def get_state(self) -> str:
        """
        Get the current game state as a string.
        
        Returns:
            String representation of the current game state
        """
        return '\n'.join(''.join(row) for row in self.grid)
    
    def _is_valid_position(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is within the grid bounds."""
        row, col = pos
        return 0 <= row < self.height and 0 <= col < self.width
    
    def _get_cell(self, pos: Tuple[int, int]) -> str:
        """Get the content of a cell."""
        if not self._is_valid_position(pos):
            return self.WALL
        return self.grid[pos[0]][pos[1]]
    
    def _set_cell(self, pos: Tuple[int, int], value: str) -> None:
        """Set the content of a cell."""
        if self._is_valid_position(pos):
            self.grid[pos[0]][pos[1]] = value
    
    def _is_wall(self, pos: Tuple[int, int]) -> bool:
        """Check if a position contains a wall."""
        return self._get_cell(pos) == self.WALL
    
    def _has_box(self, pos: Tuple[int, int]) -> bool:
        """Check if a position contains a box."""
        return self._get_cell(pos) in (self.BOX, self.BOX_ON_TARGET)
    
    def _is_target(self, pos: Tuple[int, int]) -> bool:
        """Check if a position is a target (with or without box/player)."""
        return self._get_cell(pos) in (self.TARGET, self.BOX_ON_TARGET, self.PLAYER_ON_TARGET)
    
    def _has_target(self, pos: Tuple[int, int]) -> bool:
        """Check if a position has a target symbol (including with box/player on it)."""
        return self._get_cell(pos) in (self.TARGET, self.BOX_ON_TARGET, self.PLAYER_ON_TARGET)
    
    def valid_moves(self) -> List[str]:
        """
        Get a list of valid moves from the current position.
        
        Returns:
            List of valid move directions ('up', 'down', 'left', 'right')
        """
        valid = []
        
        for direction, (dr, dc) in self.MOVES.items():
            new_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
            
            # Check if the new position is a wall
            if self._is_wall(new_pos):
                continue
                
            # Check if there's a box at the new position
            if self._has_box(new_pos):
                # Check if we can push the box
                box_new_pos = (new_pos[0] + dr, new_pos[1] + dc)
                if not self._is_wall(box_new_pos) and not self._has_box(box_new_pos):
                    valid.append(direction)
            else:
                # Empty space or target, move is valid
                valid.append(direction)
                
        return valid
    
    def take_action(self, action: str) -> bool:
        """
        Take an action (move) in the game.
        
        Args:
            action: Direction to move ('up', 'down', 'left', 'right')
            
        Returns:
            True if the action was legal and executed, False otherwise
        """
        if action not in self.MOVES:
            return False
            
        if action not in self.valid_moves():
            return False
            
        dr, dc = self.MOVES[action]
        new_pos = (self.player_pos[0] + dr, self.player_pos[1] + dc)
        
        # Remember if new position had a target before we process it
        new_pos_has_target = self._has_target(new_pos)
        
        # Handle box pushing
        if self._has_box(new_pos):
            box_new_pos = (new_pos[0] + dr, new_pos[1] + dc)
            
            # Move box to its new position
            if self._has_target(box_new_pos):
                self._set_cell(box_new_pos, self.BOX_ON_TARGET)
            else:
                self._set_cell(box_new_pos, self.BOX)
        
        # Move player from old position
        if self._get_cell(self.player_pos) == self.PLAYER_ON_TARGET:
            self._set_cell(self.player_pos, self.TARGET)
        else:
            self._set_cell(self.player_pos, self.EMPTY)
            
        # Move player to new position
        if new_pos_has_target:
            self._set_cell(new_pos, self.PLAYER_ON_TARGET)
        else:
            self._set_cell(new_pos, self.PLAYER)
            
        self.player_pos = new_pos
        return True
    
    def is_solved(self) -> bool:
        """
        Check if the puzzle is solved (all boxes are on targets).
        
        Returns:
            True if solved, False otherwise
        """
        for row in self.grid:
            for cell in row:
                if cell == self.BOX:  # Box not on target
                    return False
                if cell == self.TARGET:  # Target without box
                    return False
        return True
    
    def __str__(self) -> str:
        """String representation of the game."""
        return self.get_state()
    
    def __repr__(self) -> str:
        """Representation for debugging."""
        return f"Boxoban(size={self.width}x{self.height}, player_at={self.player_pos}, solved={self.is_solved()})"