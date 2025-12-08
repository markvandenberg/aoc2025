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


def count_splits(grid, start_pos):
    """Count unique splitter cells reached from the start."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    visited = set()
    split_seen = set()
    splits = 0

    stack = [start_pos]
    while stack:
        row, col = stack.pop()
        if (row, col) in visited:
            continue
        visited.add((row, col))

        next_row = row + 1
        if next_row >= rows:
            continue

        cell = grid[next_row][col]
        if cell == '^':
            if (next_row, col) not in split_seen:
                split_seen.add((next_row, col))
                splits += 1
            if col - 1 >= 0:
                stack.append((next_row, col - 1))
            if col + 1 < cols:
                stack.append((next_row, col + 1))
        else:
            stack.append((next_row, col))

    return splits


def solve_from(grid, row, col, memo):
    """Return (split_count, timeline_count) from a given position."""
    key = (row, col)
    if key in memo:
        return memo[key]

    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    next_row = row + 1

    if next_row >= rows:
        memo[key] = (0, 1)
        return memo[key]

    cell = grid[next_row][col]

    if cell == '^':
        splits = 1  # splitting event at this cell
        timelines = 0

        for next_col in (col - 1, col + 1):
            if 0 <= next_col < cols:
                sub_splits, sub_timelines = solve_from(grid, next_row, next_col, memo)
                splits += sub_splits
                timelines += sub_timelines
        memo[key] = (splits, timelines)
        return memo[key]

    # Empty space or S: continue straight down
    result = solve_from(grid, next_row, col, memo)
    memo[key] = result
    return result


def part1(data):
    """Count how many times the beam is split."""
    grid, start_pos = parse_input(data)
    return count_splits(grid, start_pos)


def part2(data):
    """Count the number of timelines using memoized recursion."""
    grid, start_pos = parse_input(data)
    _, timelines = solve_from(grid, start_pos[0], start_pos[1], {})
    return timelines


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
