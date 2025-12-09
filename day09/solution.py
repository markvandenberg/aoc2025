#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 9: Movie Theater
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse red tile positions."""
    lines = data.split('\n')
    tiles = []
    for line in lines:
        if line.strip():
            x, y = map(int, line.split(','))
            tiles.append((x, y))
    return tiles


def calculate_area(p1, p2):
    """Calculate area of rectangle with opposite corners at p1 and p2."""
    x1, y1 = p1
    x2, y2 = p2
    # Add 1 because we want to include both endpoints
    width = abs(x2 - x1) + 1
    height = abs(y2 - y1) + 1
    return width * height


def part1(data):
    """Find largest rectangle using two red tiles as opposite corners."""
    tiles = parse_input(data)
    
    max_area = 0
    
    # Try all pairs of tiles as opposite corners
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            area = calculate_area(tiles[i], tiles[j])
            max_area = max(max_area, area)
    
    return max_area


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
