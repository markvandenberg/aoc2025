#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 7: Laboratories
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().rstrip('\n')


def parse_input(data):
    """Parse the manifold diagram and find the starting position."""
    lines = data.split('\n')
    grid = [list(line) for line in lines]
    
    # Find starting position (S)
    start_pos = None
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == 'S':
                start_pos = (row, col)
                break
        if start_pos:
            break
    
    return grid, start_pos


def simulate_beam(grid, start_pos):
    """
    Simulate the tachyon beam splitting through the manifold.
    Returns the total number of times the beam is split.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    
    # Track active beams: list of (row, col) positions
    # Each beam moves downward one step at a time
    beams = [start_pos]
    split_count = 0
    
    # Track visited positions to avoid infinite loops
    # (though beams only move down, so this shouldn't happen)
    visited = set()
    
    while beams:
        new_beams = []
        
        for row, col in beams:
            # Skip if we've already processed this position
            if (row, col) in visited:
                continue
            visited.add((row, col))
            
            # Move down one step
            next_row = row + 1
            
            # Check if beam exits the manifold
            if next_row >= rows:
                continue
            
            # Check what's at the next position
            next_cell = grid[next_row][col]
            
            if next_cell == '^':
                # Hit a splitter! The beam splits into left and right
                split_count += 1
                
                # Create two new beams from the splitter position
                # Left beam
                if col - 1 >= 0:
                    new_beams.append((next_row, col - 1))
                
                # Right beam
                if col + 1 < cols:
                    new_beams.append((next_row, col + 1))
            
            elif next_cell == '.':
                # Empty space, beam continues downward
                new_beams.append((next_row, col))
            
            elif next_cell == 'S':
                # This shouldn't happen since S is the start
                new_beams.append((next_row, col))
        
        beams = new_beams
    
    return split_count


def part1(data):
    """Count how many times the beam is split."""
    grid, start_pos = parse_input(data)
    return simulate_beam(grid, start_pos)


def part2(data):
    """Solve part 2 (not yet revealed)."""
    return 0


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
