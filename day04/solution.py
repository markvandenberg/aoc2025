#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 4: Printing Department
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the input data into a 2D grid."""
    return [list(line) for line in data.split('\n')]


def count_adjacent_rolls(grid, row, col):
    """Count the number of paper rolls (@) in the 8 adjacent positions."""
    rows = len(grid)
    cols = len(grid[0])
    
    # 8 directions: up, down, left, right, and 4 diagonals
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]
    
    count = 0
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        
        # Check if position is within bounds
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row][new_col] == '@':
                count += 1
    
    return count


def part1(data):
    """Count how many rolls of paper can be accessed by a forklift.
    
    A roll can be accessed if there are fewer than 4 rolls in adjacent positions.
    """
    grid = parse_input(data)
    rows = len(grid)
    cols = len(grid[0])
    
    accessible_count = 0
    
    for row in range(rows):
        for col in range(cols):
            # Only check positions that have a paper roll
            if grid[row][col] == '@':
                adjacent_count = count_adjacent_rolls(grid, row, col)
                
                # Can access if fewer than 4 adjacent rolls
                if adjacent_count < 4:
                    accessible_count += 1
    
    return accessible_count


def part2(data):
    """Count total rolls that can be removed by repeatedly removing accessible rolls.
    
    Keep removing accessible rolls (< 4 adjacent) until no more can be removed.
    """
    grid = parse_input(data)
    rows = len(grid)
    cols = len(grid[0])
    
    total_removed = 0
    
    while True:
        # Find all accessible rolls in current state
        accessible = []
        
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == '@':
                    adjacent_count = count_adjacent_rolls(grid, row, col)
                    if adjacent_count < 4:
                        accessible.append((row, col))
        
        # If no more accessible rolls, stop
        if not accessible:
            break
        
        # Remove all accessible rolls
        for row, col in accessible:
            grid[row][col] = '.'
        
        total_removed += len(accessible)
    
    return total_removed


def main():
    import sys
    # Read input (use command line argument if provided, otherwise default to input.txt)
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    data = read_input(filename)
    
    # Solve parts
    result1 = part1(data)
    print(f"Part 1: {result1}")
    
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
