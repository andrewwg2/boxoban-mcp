"""Tests for the Boxoban game implementation."""

import pytest
from pathlib import Path
import tempfile
from src.boxoban_mcp import Boxoban


class TestBoxobanBasics:
    """Test basic Boxoban functionality."""
    
    def test_from_string(self):
        """Test creating a game from string."""
        game_str = """##########
#   @    #
#   $    #
#   .    #
##########"""
        
        game = Boxoban.from_string(game_str)
        assert game.player_pos == (1, 4)
        assert game.get_state() == game_str
    
    def test_symbols(self):
        """Test that all symbols are correctly recognized."""
        game_str = """##########
#  @$    #
#  *.+   #
#        #
##########"""
        
        game = Boxoban.from_string(game_str)
        state = game.get_state()
        assert '@' in state  # Player
        assert '$' in state  # Box
        assert '*' in state  # Box on target
        assert '+' in state  # Player on target
        # Note: bare '.' should not appear when covered by * or +
    
    def test_player_position(self):
        """Test finding player position."""
        game_str = """#####
# @ #
#####"""
        
        game = Boxoban.from_string(game_str)
        assert game.player_pos == (1, 2)
        
        # Test with player on target
        game_str2 = """#####
# + #
#####"""
        
        game2 = Boxoban.from_string(game_str2)
        assert game2.player_pos == (1, 2)


class TestMovement:
    """Test movement and collision logic."""
    
    def test_basic_movement(self):
        """Test basic player movement in empty space."""
        game_str = """#####
# @ #
#   #
#####"""
        
        game = Boxoban.from_string(game_str)
        
        # Test valid moves from initial position
        valid = game.valid_moves()
        assert 'down' in valid      # Space below
        assert 'up' not in valid    # Wall above
        assert 'left' in valid      # Space to left
        assert 'right' in valid     # Space to right
        
        # Execute move down
        assert game.take_action('down') == True
        assert game.player_pos == (2, 2)
        
        # Check new valid moves
        valid = game.valid_moves()
        assert 'up' in valid
        assert 'down' not in valid  # Wall below
        assert 'left' in valid      # Space to left
        assert 'right' in valid     # Space to right
    
    def test_wall_collision(self):
        """Test that player cannot move into walls."""
        game_str = """#####
#@ ##
#####"""
        
        game = Boxoban.from_string(game_str)
        valid = game.valid_moves()
        
        assert 'left' not in valid  # Wall to left
        assert 'right' in valid     # Space to right
        assert 'up' not in valid    # Wall above
        assert 'down' not in valid  # Wall below
        
        # Try invalid move
        assert game.take_action('left') == False
        assert game.player_pos == (1, 1)  # Position unchanged
    
    def test_box_pushing(self):
        """Test pushing boxes."""
        game_str = """######
#  @ #
#  $ #
#    #
######"""
        
        game = Boxoban.from_string(game_str)
        
        # Move down to push box
        assert 'down' in game.valid_moves()
        assert game.take_action('down') == True
        
        # Check positions
        assert game.player_pos == (2, 3)
        state_lines = game.get_state().split('\n')
        assert state_lines[2][3] == '@'  # Player moved to box position
        assert state_lines[3][3] == '$'  # Box pushed down
    
    def test_box_into_wall(self):
        """Test that boxes cannot be pushed into walls."""
        game_str = """#####
# @$#
#####"""
        
        game = Boxoban.from_string(game_str)
        
        # Cannot push box into wall
        assert 'right' not in game.valid_moves()
        assert game.take_action('right') == False
    
    def test_box_into_box(self):
        """Test that boxes cannot be pushed into other boxes."""
        game_str = """######
# @$$ #
######"""
        
        game = Boxoban.from_string(game_str)
        
        # Cannot push box into another box
        assert 'right' not in game.valid_moves()
    
    def test_box_onto_target(self):
        """Test pushing box onto target."""
        game_str = """#####
#    #
# @  #
# $  #
# .  #
#####"""
        
        game = Boxoban.from_string(game_str)
        
        # Push box down onto target
        assert game.take_action('down') == True
        
        state_lines = game.get_state().split('\n')
        assert state_lines[3][2] == '@'  # Player moved to where box was
        assert state_lines[4][2] == '*'  # Box on target
    
    def test_player_onto_target(self):
        """Test player moving onto target."""
        game_str = """#####
# @ #
# . #
#####"""
        
        game = Boxoban.from_string(game_str)
        
        assert game.take_action('down') == True
        state_lines = game.get_state().split('\n')
        assert state_lines[2][2] == '+'  # Player on target
    
    def test_leaving_target(self):
        """Test player/box leaving target restores target."""
        # Test player leaving target
        game_str = """#####
# + #
#   #
#####"""
        
        game = Boxoban.from_string(game_str)
        assert game.take_action('down') == True
        
        state_lines = game.get_state().split('\n')
        assert state_lines[1][2] == '.'  # Target restored
        assert state_lines[2][2] == '@'  # Player moved
        
        # Test box leaving target by pushing it
        game_str2 = """######
# @* #
#    #
######"""
        
        game2 = Boxoban.from_string(game_str2)
        # Push box to the right (player moves right, pushes box right)
        assert game2.take_action('right') == True
        
        state_lines = game2.get_state().split('\n')
        assert state_lines[1][3] == '+'  # Player on target where box was
        assert state_lines[1][4] == '$'  # Box moved off target to the right


class TestGameState:
    """Test game state management."""
    
    def test_is_solved(self):
        """Test puzzle solved detection."""
        # Not solved - box not on target
        game_str = """#####
# @$ #
# .  #
#####"""
        
        game = Boxoban.from_string(game_str)
        assert not game.is_solved()
        
        # Solved - all boxes on targets
        game_str2 = """#####
# @* #
#    #
#####"""
        
        game2 = Boxoban.from_string(game_str2)
        assert game2.is_solved()
        
        # Not solved - target without box
        game_str3 = """#####
# @* #
# .  #
#####"""
        
        game3 = Boxoban.from_string(game_str3)
        assert not game3.is_solved()
    
    def test_complex_puzzle_solved(self):
        """Test with multiple boxes and targets."""
        # All boxes on targets
        game_str = """######
# @  #
# ** #
# ** #
######"""
        
        game = Boxoban.from_string(game_str)
        assert game.is_solved()
        
        # One box not on target
        game_str2 = """######
# @$ #
# ** #
# *. #
######"""
        
        game2 = Boxoban.from_string(game_str2)
        assert not game2.is_solved()


class TestLoaders:
    """Test different loading methods."""
    
    def test_from_file(self):
        """Test loading from file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("""; 0
##########
#   @    #
#   $    #
#   .    #
##########

; 1
#####
# @ #
#####""")
            temp_path = f.name
        
        try:
            game = Boxoban.from_file(temp_path)
            # Should load first puzzle
            assert game.player_pos == (1, 4)
            assert game.height == 5
            assert game.width == 10
        finally:
            Path(temp_path).unlink()
    
    def test_from_puzzle_path(self):
        """Test loading from puzzle directory structure."""
        # Test with an actual puzzle file
        game = Boxoban.from_puzzle_path('medium', 'valid', '000', 0)
        
        # Verify it loaded something
        assert game.player_pos is not None
        assert game.height > 0
        assert game.width > 0
        
        # Test loading a different puzzle from same file
        game2 = Boxoban.from_puzzle_path('medium', 'valid', '000', 1)
        assert game.get_state() != game2.get_state()  # Different puzzles
    
    def test_padding(self):
        """Test that lines are padded to consistent width."""
        game_str = """###
#@#
# .#
###"""
        
        game = Boxoban.from_string(game_str)
        lines = game.get_state().split('\n')
        
        # All lines should have same length
        assert all(len(line) == len(lines[0]) for line in lines)


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_no_player(self):
        """Test error when no player in game."""
        game_str = """#####
#   #
#####"""
        
        with pytest.raises(ValueError, match="No player found"):
            Boxoban.from_string(game_str)
    
    def test_invalid_action(self):
        """Test invalid action names."""
        game_str = """#####
# @ #
#####"""
        
        game = Boxoban.from_string(game_str)
        assert game.take_action('invalid') == False
        assert game.take_action('UP') == False  # Case sensitive
    
    def test_empty_game(self):
        """Test empty game string."""
        with pytest.raises(ValueError):
            Boxoban.from_string("")
    
    def test_all_directions(self):
        """Test all four movement directions."""
        game_str = """#####
#   #
# @ #
#   #
#####"""
        
        game = Boxoban.from_string(game_str)
        
        valid = game.valid_moves()
        assert set(valid) == {'up', 'down', 'left', 'right'}
        
        # Test each direction
        initial_pos = game.player_pos
        
        assert game.take_action('up')
        assert game.player_pos == (initial_pos[0] - 1, initial_pos[1])
        
        assert game.take_action('right')
        assert game.player_pos == (initial_pos[0] - 1, initial_pos[1] + 1)
        
        assert game.take_action('down')
        assert game.player_pos == (initial_pos[0], initial_pos[1] + 1)
        
        assert game.take_action('left')
        assert game.player_pos == initial_pos