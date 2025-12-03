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
    """Find the maximum joltage possible from a battery bank.
    
    We need to pick exactly 2 batteries (digits) to maximize the value.
    This means picking the two largest digits in order.
    """
    # Find the two positions with the largest digits
    best = 0
    
    # Try all pairs of positions
    for i in range(len(bank)):
        for j in range(i + 1, len(bank)):
            # Form the number from batteries at positions i and j
            value = int(bank[i] + bank[j])
            best = max(best, value)
    
    return best


def part1(data):
    """Find the maximum joltage from each bank and sum them."""
    banks = parse_input(data)
    
    total = 0
    for bank in banks:
        total += max_joltage(bank)
    
    return total


def max_joltage_n_batteries(bank, n):
    """Find the maximum joltage possible by selecting exactly n batteries.
    
    To maximize the resulting number, we want:
    1. The leftmost digits to be as large as possible
    2. This means we should skip the smallest digits
    
    Strategy: Remove (len(bank) - n) smallest digits while maintaining order.
    """
    if n >= len(bank):
        return int(bank)
    
    digits_to_remove = len(bank) - n
    bank_list = list(bank)
    
    # Greedily remove the smallest digits while maintaining order
    # We want to keep the lexicographically largest subsequence of length n
    for _ in range(digits_to_remove):
        # Find the position to remove: we want to remove the first digit
        # that is smaller than the digit after it (or the last digit if none found)
        removed = False
        for i in range(len(bank_list) - 1):
            if bank_list[i] < bank_list[i + 1]:
                bank_list.pop(i)
                removed = True
                break
        
        # If we didn't find any digit smaller than the next, remove the last digit
        if not removed:
            bank_list.pop()
    
    return int(''.join(bank_list))


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
