#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 5: Cafeteria
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the input into fresh ranges and available IDs."""
    parts = data.split('\n\n')
    
    # Parse fresh ranges
    fresh_ranges = []
    for line in parts[0].split('\n'):
        start, end = map(int, line.split('-'))
        fresh_ranges.append((start, end))
    
    # Parse available IDs
    available_ids = []
    for line in parts[1].split('\n'):
        available_ids.append(int(line))
    
    return fresh_ranges, available_ids


def is_fresh(ingredient_id, fresh_ranges):
    """Check if an ingredient ID is fresh (falls into any range)."""
    for start, end in fresh_ranges:
        if start <= ingredient_id <= end:
            return True
    return False


def part1(data):
    """Count how many available ingredient IDs are fresh."""
    fresh_ranges, available_ids = parse_input(data)
    
    fresh_count = 0
    for ingredient_id in available_ids:
        if is_fresh(ingredient_id, fresh_ranges):
            fresh_count += 1
    
    return fresh_count


def part2(data):
    """Count total unique ingredient IDs that are considered fresh by the ranges.
    
    We need to merge overlapping ranges and count all IDs they cover.
    """
    fresh_ranges, _ = parse_input(data)
    
    # Sort ranges by start position
    fresh_ranges.sort()
    
    # Merge overlapping ranges
    merged = []
    for start, end in fresh_ranges:
        if merged and start <= merged[-1][1] + 1:
            # Overlaps or adjacent with previous range, merge them
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            # No overlap, add as new range
            merged.append((start, end))
    
    # Count total IDs in all merged ranges
    total = 0
    for start, end in merged:
        total += (end - start + 1)
    
    return total


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
