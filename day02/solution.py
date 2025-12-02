#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 2: Gift Shop
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the input data into list of (start, end) ranges."""
    ranges = []
    for range_str in data.replace('\n', '').split(','):
        if range_str.strip():
            start, end = range_str.strip().split('-')
            ranges.append((int(start), int(end)))
    return ranges


def is_invalid_id(num):
    """Check if a number is made of some sequence of digits repeated twice."""
    s = str(num)
    length = len(s)
    
    # Must be even length to be split in half
    if length % 2 != 0:
        return False
    
    # Check if first half equals second half
    mid = length // 2
    first_half = s[:mid]
    second_half = s[mid:]
    
    return first_half == second_half


def part1(data):
    """Find all invalid IDs in the given ranges and sum them."""
    ranges = parse_input(data)
    
    total = 0
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id(num):
                total += num
    
    return total


def is_invalid_id_part2(num):
    """Check if a number is made of some sequence of digits repeated at least twice."""
    s = str(num)
    length = len(s)
    
    # Try all possible pattern lengths (from 1 to length//2)
    for pattern_len in range(1, length // 2 + 1):
        # Check if the length is divisible by pattern_len
        if length % pattern_len == 0:
            pattern = s[:pattern_len]
            # Check if the entire string is this pattern repeated
            repeats = length // pattern_len
            if repeats >= 2 and pattern * repeats == s:
                return True
    
    return False


def part2(data):
    """Find all invalid IDs (repeated at least twice) in the given ranges and sum them."""
    ranges = parse_input(data)
    
    total = 0
    for start, end in ranges:
        for num in range(start, end + 1):
            if is_invalid_id_part2(num):
                total += num
    
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
