#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 6: Trash Compactor
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().rstrip('\n')


def parse_input(data):
    """Parse the worksheet into individual problems.
    
    Problems are arranged vertically in columns, separated by empty columns.
    """
    lines = data.split('\n')
    
    if not lines:
        return []
    
    # Find the width (length of the longest line)
    width = max(len(line) for line in lines)
    
    # Pad all lines to the same width
    padded_lines = [line.ljust(width) for line in lines]
    
    problems = []
    col = 0
    
    while col < width:
        # Skip empty columns
        if all(line[col] == ' ' for line in padded_lines):
            col += 1
            continue
        
        # Found start of a problem, collect all columns until we hit an empty column
        problem_cols = []
        while col < width and not all(line[col] == ' ' for line in padded_lines):
            problem_cols.append(col)
            col += 1
        
        # Extract the problem from these columns
        problem_lines = []
        for line in padded_lines:
            problem_text = ''.join(line[c] for c in problem_cols).strip()
            if problem_text:
                problem_lines.append(problem_text)
        
        if problem_lines:
            # Last line is the operator, rest are numbers
            operator = problem_lines[-1]
            numbers = [int(num) for num in problem_lines[:-1]]
            problems.append((numbers, operator))
    
    return problems


def solve_problem(numbers, operator):
    """Solve a single problem by applying the operator to all numbers."""
    if operator == '+':
        return sum(numbers)
    elif operator == '*':
        result = 1
        for num in numbers:
            result *= num
        return result
    else:
        raise ValueError(f"Unknown operator: {operator}")


def part1(data):
    """Solve all problems and return the grand total."""
    problems = parse_input(data)
    
    grand_total = 0
    for numbers, operator in problems:
        answer = solve_problem(numbers, operator)
        grand_total += answer
    
    return grand_total


def part2(data):
    """Solve part 2."""
    problems = parse_input(data)
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
