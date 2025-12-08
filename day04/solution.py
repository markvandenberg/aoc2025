#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 4: Printing Department
"""

from collections import deque


DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1),
]


def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the input data into a 2D grid."""
    return [list(line) for line in data.split('\n')]


def compute_adjacent_counts(grid):
    """Precompute adjacent roll counts for every cell."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    counts = [[0] * cols for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] != '@':
                continue

            neighbor_count = 0
            for dr, dc in DIRECTIONS:
                nr = row + dr
                nc = col + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                    neighbor_count += 1
            counts[row][col] = neighbor_count

    return counts


def part1(data):
    """Count how many rolls of paper can be accessed by a forklift.
    
    A roll can be accessed if there are fewer than 4 rolls in adjacent positions.
    """
    grid = parse_input(data)
    counts = compute_adjacent_counts(grid)

    accessible_count = 0
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == '@' and counts[row][col] < 4:
                accessible_count += 1

    return accessible_count


def part2(data):
    """Count total rolls that can be removed by repeatedly removing accessible rolls.
    
    Keep removing accessible rolls (< 4 adjacent) until no more can be removed.
    """
    grid = parse_input(data)
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    counts = compute_adjacent_counts(grid)

    queue = deque()
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '@' and counts[row][col] < 4:
                queue.append((row, col))

    total_removed = 0

    while queue:
        row, col = queue.popleft()
        if grid[row][col] != '@':
            continue
        if counts[row][col] >= 4:
            continue

        grid[row][col] = '.'
        total_removed += 1

        for dr, dc in DIRECTIONS:
            nr = row + dr
            nc = col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '@':
                counts[nr][nc] -= 1
                if counts[nr][nc] == 3:
                    queue.append((nr, nc))

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
