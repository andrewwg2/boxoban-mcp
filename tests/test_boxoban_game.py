"""Tests for the BoxobanGame class."""

import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.boxoban_mcp.game import BoxobanGame, Direction


class TestBoxobanGame:
    """Test suite for BoxobanGame class."""
    
    def test_from_string_basic(self):
        """Test creating a game from a string."""
        puzzle = """
##########
#     @  #
#  $ $. .#
#    $. .#
##########
"""
        game = BoxobanGame.from_string(puzzle)
        
        assert game.player_pos == (1, 6)
        assert len(game.boxes) == 3
        assert len(game.goals) == 4
        assert game.height == 5
        assert game.width == 10
    
    def test_from_string_with_number(self):
        """Test creating a game from a string with puzzle number."""
        puzzle = """; 0
##########
#     @  #
#  $ $. .#
#    $. .#
##########
"""
        game = BoxobanGame.from_string(puzzle)
        
        assert game.player_pos == (1, 6)
        assert len(game.boxes) == 3
        assert len(game.goals) == 4
    
    def test_get_state(self):
        """Test getting the current game state."""
        puzzle = """
#####
#@$.#
#####
"""
        game = BoxobanGame.from_string(puzzle)
        state = game.get_state()
        
        assert state[1][1] == '@'
        assert state[1][2] == '$'
        assert state[1][3] == '.'
    
    def test_valid_moves_open_space(self):
        """Test valid moves when player has open space around."""
        puzzle = """
#####
# @ #
#   #
#####
"""
        game = BoxobanGame.from_string(puzzle)
        valid = game.valid_moves()
        
        # Should be able to move in all directions except up (wall)
        assert Direction.DOWN in valid
        assert Direction.LEFT in valid
        assert Direction.RIGHT in valid
        assert Direction.UP not in valid
    
    def test_valid_moves_walls(self):
        """Test valid moves when surrounded by walls."""
        puzzle = """
#####
##@##
#####
"""
        game = BoxobanGame.from_string(puzzle)
        valid = game.valid_moves()
        
        assert len(valid) == 0
    
    def test_valid_moves_push_box(self):
        """Test valid moves when pushing boxes."""
        puzzle = """
######
#    #
# @$ #
#    #
######
"""
        game = BoxobanGame.from_string(puzzle)
        valid = game.valid_moves()
        
        # Can push box right, but not into other directions with box
        assert Direction.RIGHT in valid
        assert Direction.UP in valid
        assert Direction.DOWN in valid
        assert Direction.LEFT in valid
    
    def test_valid_moves_box_against_wall(self):
        """Test that can't push box into wall."""
        puzzle = """
#####
# @$#
#####
"""
        game = BoxobanGame.from_string(puzzle)
        valid = game.valid_moves()
        
        # Can't push box right into wall
        assert Direction.RIGHT not in valid
        assert Direction.LEFT in valid
    
    def test_valid_moves_box_against_box(self):
        """Test that can't push box into another box."""
        puzzle = """
######
# @$$#
######
"""
        game = BoxobanGame.from_string(puzzle)
        valid = game.valid_moves()
        
        # Can't push box right into another box
        assert Direction.RIGHT not in valid
        assert Direction.LEFT in valid
    
    def test_take_action_move(self):
        """Test taking a simple move action."""
        puzzle = """
#####
# @ #
#####
"""
        game = BoxobanGame.from_string(puzzle)
        
        assert game.take_action(Direction.LEFT)
        assert game.player_pos == (1, 1)
        
        # Invalid move into wall
        assert not game.take_action(Direction.LEFT)
        assert game.player_pos == (1, 1)
    
    def test_take_action_push_box(self):
        """Test pushing a box."""
        puzzle = """
######
#  @ #
#  $ #
#  . #
######
"""
        game = BoxobanGame.from_string(puzzle)
        initial_state = game.get_state()
        
        # Push box down
        assert game.take_action(Direction.DOWN)
        assert game.player_pos == (2, 3)
        assert (3, 3) in game.boxes
        assert (2, 3) not in game.boxes
        
        # Verify goal is still there
        assert (3, 3) in game.goals
    
    def test_take_action_invalid(self):
        """Test that invalid actions return False."""
        puzzle = """
###
#@#
###
"""
        game = BoxobanGame.from_string(puzzle)
        
        assert not game.take_action(Direction.UP)
        assert not game.take_action(Direction.DOWN)
        assert not game.take_action(Direction.LEFT)
        assert not game.take_action(Direction.RIGHT)
    
    def test_is_solved(self):
        """Test checking if puzzle is solved."""
        puzzle = """
#####
#@$.#
#####
"""
        game = BoxobanGame.from_string(puzzle)
        
        assert not game.is_solved()
        
        # Push box onto goal
        game.take_action(Direction.RIGHT)
        assert game.is_solved()
    
    def test_box_on_goal_symbol(self):
        """Test that box on goal shows correct symbol."""
        puzzle = """
#####
#   #
#@$.#
#####
"""
        game = BoxobanGame.from_string(puzzle)
        
        # Push box right onto goal
        game.take_action(Direction.RIGHT)
        
        state = game.get_state()
        assert state[2][3] == '*'  # Box on goal
    
    def test_player_on_goal_symbol(self):
        """Test that player on goal shows correct symbol."""
        puzzle = """
#####
#@. #
#####
"""
        game = BoxobanGame.from_string(puzzle)
        
        # Move player onto goal
        game.take_action(Direction.RIGHT)
        
        state = game.get_state()
        assert state[1][2] == '+'  # Player on goal
    
    def test_copy(self):
        """Test creating a copy of the game."""
        puzzle = """
#####
#@$.#
#####
"""
        game1 = BoxobanGame.from_string(puzzle)
        game2 = game1.copy()
        
        # Modify game1
        game1.take_action(Direction.RIGHT)
        
        # game2 should be unchanged
        assert game1.player_pos != game2.player_pos
        assert game1.boxes != game2.boxes
    
    def test_from_file(self):
        """Test loading from a file."""
        # This test assumes the puzzle files exist
        try:
            game = BoxobanGame.from_file('puzzles/hard/000.txt')
            assert game.player_pos is not None
            assert len(game.boxes) == 4  # All puzzles have 4 boxes
            assert len(game.goals) == 4  # All puzzles have 4 goals
        except FileNotFoundError:
            pytest.skip("Puzzle files not found")
    
    def test_from_parameters(self):
        """Test loading using parameters."""
        try:
            game = BoxobanGame.from_parameters('hard', None, '000', 0)
            assert game.player_pos is not None
            assert len(game.boxes) == 4
            assert len(game.goals) == 4
            
            # Test medium puzzle
            game2 = BoxobanGame.from_parameters('medium', 'train', '000', 1)
            assert game2.player_pos is not None
            assert len(game2.boxes) == 4
            assert len(game2.goals) == 4
        except FileNotFoundError:
            pytest.skip("Puzzle files not found")
    
    def test_complex_scenario(self):
        """Test a more complex game scenario."""
        puzzle = """
########
#      #
# .$. @#
#  $  ##
# .$. ##
#     ##
########
"""
        game = BoxobanGame.from_string(puzzle)
        
        # Initial state
        assert len(game.boxes) == 3
        assert len(game.goals) == 4
        assert not game.is_solved()
        
        # Move left and push middle box
        game.take_action(Direction.LEFT)
        game.take_action(Direction.LEFT)
        game.take_action(Direction.LEFT)
        game.take_action(Direction.DOWN)
        
        # Check state after moves
        state = game.get_state()
        print("\nGame state after moves:")
        print(game)
        
        # Continue solving...
        moves = [Direction.LEFT, Direction.UP, Direction.RIGHT, 
                Direction.DOWN, Direction.RIGHT, Direction.DOWN]
        
        for move in moves:
            if move in game.valid_moves():
                game.take_action(move)
    
    def test_string_representation(self):
        """Test string representation of the game."""
        puzzle = """
#####
#@$.#
#####
"""
        game = BoxobanGame.from_string(puzzle)
        
        str_repr = str(game)
        lines = str_repr.strip().split('\n')
        
        assert len(lines) == 3
        assert lines[1] == '#@$.#'