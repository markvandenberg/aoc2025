#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 1: Secret Entrance
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the input data into list of (direction, distance) tuples."""
    rotations = []
    for line in data.split('\n'):
        direction = line[0]  # 'L' or 'R'
        distance = int(line[1:])
        rotations.append((direction, distance))
    return rotations


def part1(data):
    """Count how many times the dial points at 0 after any rotation."""
    rotations = parse_input(data)
    
    position = 50  # Starting position
    zero_count = 0
    
    for direction, distance in rotations:
        if direction == 'L':
            position = (position - distance) % 100
        else:  # direction == 'R'
            position = (position + distance) % 100
        
        # Check if dial is pointing at 0
        if position == 0:
            zero_count += 1
    
    return zero_count


def part2(data):
    """Solve part 2."""
    parsed = parse_input(data)
    # TODO: Implement solution when part 2 is unlocked
    return None


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
