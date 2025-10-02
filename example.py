#!/usr/bin/env python3
"""Example usage of the BoxobanGame class."""

from src.boxoban_mcp.game import BoxobanGame, Direction

def main():
    # Example 1: Simple puzzle
    print("=== Example 1: Simple Puzzle ===")
    puzzle = """
#######
#     #
# @$. #
#     #
#######
"""
    game = BoxobanGame.from_string(puzzle)
    print("Initial state:")
    print(game)
    print(f"\nValid moves: {[d.name for d in game.valid_moves()]}")
    
    # Push the box onto the goal
    print("\nPushing box RIGHT onto goal...")
    game.take_action(Direction.RIGHT)
    print(game)
    print(f"Solved: {game.is_solved()}")
    
    # Example 2: More complex puzzle
    print("\n\n=== Example 2: Complex Puzzle ===")
    puzzle2 = """
########
# .    #
# @$$. #
#  $$. #
# .    #
########
"""
    game2 = BoxobanGame.from_string(puzzle2)
    print("Initial state:")
    print(game2)
    
    # Demonstrate invalid move
    print(f"\nValid moves: {[d.name for d in game2.valid_moves()]}")
    print("\nTrying to move UP (should fail - wall):")
    success = game2.take_action(Direction.UP)
    print(f"Move successful: {success}")
    
    # Demonstrate valid move
    print("\nMoving RIGHT:")
    success = game2.take_action(Direction.RIGHT)
    print(f"Move successful: {success}")
    print(game2)
    
    # Example 3: Loading from file (if available)
    print("\n\n=== Example 3: Loading from File ===")
    try:
        game3 = BoxobanGame.from_parameters('hard', None, '000', 0)
        print("Loaded puzzle from hard/000.txt, puzzle 0:")
        print(game3)
        print(f"Number of boxes: {len(game3.boxes)}")
        print(f"Number of goals: {len(game3.goals)}")
    except FileNotFoundError:
        print("Puzzle files not found - skipping file loading example")

if __name__ == "__main__":
    main()