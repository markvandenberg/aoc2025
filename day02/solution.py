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


def arithmetic_sum(a, b):
    """Return the sum of the inclusive range [a, b]."""
    return (a + b) * (b - a + 1) // 2


def divisors(n):
    """Return sorted divisors of n."""
    small = []
    large = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            small.append(i)
            if i * i != n:
                large.append(n // i)
        i += 1
    return small + large[::-1]


def sum_repeated_numbers(ranges, min_repeat=2, max_repeat=None):
    """Sum numbers that consist of a base pattern repeated."""
    contributions = {}

    for start, end in ranges:
        if start > end:
            start, end = end, start

        digits_min = len(str(start))
        digits_max = len(str(end))

        for total_digits in range(digits_min, digits_max + 1):
            lower_bound = 10 ** (total_digits - 1)
            upper_bound = 10 ** total_digits - 1
            lo = max(start, lower_bound)
            hi = min(end, upper_bound)
            if lo > hi:
                continue

            for block_len in divisors(total_digits):
                repeats = total_digits // block_len
                if repeats < min_repeat:
                    continue
                if max_repeat is not None and repeats > max_repeat:
                    continue

                pattern_min = 10 ** (block_len - 1)
                pattern_max = 10 ** block_len - 1
                multiplier = (10 ** total_digits - 1) // (10 ** block_len - 1)

                low_pattern = max(pattern_min, (lo + multiplier - 1) // multiplier)
                high_pattern = min(pattern_max, hi // multiplier)
                if low_pattern > high_pattern:
                    continue

                key = (total_digits, block_len)
                contributions[key] = contributions.get(key, 0) + (
                    multiplier * arithmetic_sum(low_pattern, high_pattern)
                )

    total = 0

    digits_to_blocks = {}
    for (digits, block_len), value in contributions.items():
        digits_to_blocks.setdefault(digits, {})
        digits_to_blocks[digits][block_len] = (
            digits_to_blocks[digits].get(block_len, 0) + value
        )

    for digits in sorted(digits_to_blocks):
        block_values = digits_to_blocks[digits]
        primitive = {}
        for block_len in sorted(block_values):
            value = block_values[block_len]
            for smaller_len, smaller_value in primitive.items():
                if block_len % smaller_len == 0:
                    value -= smaller_value
            primitive[block_len] = value
            total += value

    return total


def part1(data):
    """Find all invalid IDs in the given ranges and sum them."""
    ranges = parse_input(data)
    return sum_repeated_numbers(ranges, min_repeat=2, max_repeat=2)


def part2(data):
    """Find all invalid IDs (repeated at least twice) in the given ranges and sum them."""
    ranges = parse_input(data)
    return sum_repeated_numbers(ranges, min_repeat=2)


def main():
    import sys

    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    data = read_input(filename)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
