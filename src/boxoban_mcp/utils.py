"""Utility functions for Boxoban game."""

from typing import List, Dict


def count_game_elements(game_state: str) -> Dict[str, int]:
    """
    Count the number of each game element in a game state.
    
    Args:
        game_state: String representation of the game
        
    Returns:
        Dictionary with counts of each element
    """
    counts = {
        'walls': 0,
        'player': 0,
        'boxes': 0,
        'targets': 0,
        'boxes_on_targets': 0,
        'player_on_target': 0,
        'empty': 0
    }
    
    for char in game_state:
        if char == '#':
            counts['walls'] += 1
        elif char == '@':
            counts['player'] += 1
        elif char == '$':
            counts['boxes'] += 1
        elif char == '.':
            counts['targets'] += 1
        elif char == '*':
            counts['boxes_on_targets'] += 1
        elif char == '+':
            counts['player_on_target'] += 1
        elif char == ' ':
            counts['empty'] += 1
    
    return counts


def validate_puzzle(game_state: str) -> List[str]:
    """
    Validate a puzzle for common issues.
    
    Args:
        game_state: String representation of the game
        
    Returns:
        List of validation messages (empty if valid)
    """
    errors = []
    counts = count_game_elements(game_state)
    
    # Check for player
    total_players = counts['player'] + counts['player_on_target']
    if total_players == 0:
        errors.append("No player found in puzzle")
    elif total_players > 1:
        errors.append(f"Multiple players found: {total_players}")
    
    # Check boxes vs targets
    total_boxes = counts['boxes'] + counts['boxes_on_targets']
    total_targets = counts['targets'] + counts['boxes_on_targets'] + counts['player_on_target']
    
    if total_boxes != total_targets:
        errors.append(f"Box/target mismatch: {total_boxes} boxes, {total_targets} targets")
    
    return errors


def get_symbol_legend() -> str:
    """Get a formatted legend of game symbols."""
    return """Game Symbols:
    # - Wall
    @ - Player
    $ - Box
    . - Target/destination
    * - Box on target
    + - Player on target
      - Empty space"""