#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 3: Lobby
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the input data into list of battery banks."""
    return data.split('\n')


def max_joltage(bank):
    """Find the maximum joltage possible from a battery bank."""
    if len(bank) < 2:
        return int(bank or 0)

    digits = [int(ch) for ch in bank]
    max_suffix = [0] * len(digits)
    running_max = digits[-1]
    max_suffix[-1] = running_max

    # Precompute the best digit available to the right of each position.
    for idx in range(len(digits) - 2, -1, -1):
        running_max = max(running_max, digits[idx])
        max_suffix[idx] = running_max

    best = 0
    for idx in range(len(digits) - 1):
        candidate = digits[idx] * 10 + max_suffix[idx + 1]
        if candidate > best:
            best = candidate
    return best


def part1(data):
    """Find the maximum joltage from each bank and sum them."""
    banks = parse_input(data)
    
    total = 0
    for bank in banks:
        total += max_joltage(bank)
    
    return total


def max_joltage_n_batteries(bank, n):
    """Find the maximum joltage possible by selecting exactly n batteries."""
    if n >= len(bank):
        return int(bank)

    to_remove = len(bank) - n
    stack = []

    # Monotonic stack that drops smaller digits when a larger digit appears.
    for digit in bank:
        while to_remove and stack and stack[-1] < digit:
            stack.pop()
            to_remove -= 1
        stack.append(digit)

    if to_remove:
        stack = stack[:-to_remove]

    return int(''.join(stack[:n]))


def part2(data):
    """Find the maximum joltage from each bank using 12 batteries and sum them."""
    banks = parse_input(data)
    
    total = 0
    for bank in banks:
        total += max_joltage_n_batteries(bank, 12)
    
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
