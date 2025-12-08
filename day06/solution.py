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
    empty_cols = [all(line[col] == ' ' for line in padded_lines) for col in range(width)]

    problems = []
    col = 0

    while col < width:
        if empty_cols[col]:
            col += 1
            continue

        problem_cols = []
        while col < width and not empty_cols[col]:
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


def parse_input_rtl(data):
    """Parse the worksheet reading right-to-left, column by column.
    
    In cephalopod math:
    - Each COLUMN represents ONE COMPLETE NUMBER
    - Read each column top-to-bottom (top = most significant, bottom = least significant)
    - Problems are groups of columns separated by empty columns
    - Read problems right-to-left
    """
    lines = data.split('\n')
    
    if not lines:
        return []
    
    # Find the width
    width = max(len(line) for line in lines)
    
    # Pad all lines to the same width
    padded_lines = [line.ljust(width) for line in lines]
    empty_cols = [all(line[col] == ' ' for line in padded_lines) for col in range(width)]

    problems = []
    col = width - 1  # Start from the rightmost column

    while col >= 0:
        if empty_cols[col]:
            col -= 1
            continue

        problem_cols = []
        while col >= 0 and not empty_cols[col]:
            problem_cols.append(col)
            col -= 1
        
        # Each column in problem_cols represents one complete number
        # Read each column top-to-bottom
        numbers = []
        operator = None
        
        for col_idx in problem_cols:
            # Read this column top-to-bottom to form a number
            number_str = ''
            for row_idx in range(len(padded_lines) - 1):  # All rows except last
                char = padded_lines[row_idx][col_idx]
                if char != ' ':
                    number_str += char
            
            if number_str:
                numbers.append(int(number_str))
        
        # Last row has the operator - check any column in this problem
        operator_line = padded_lines[-1]
        for col_idx in problem_cols:
            char = operator_line[col_idx]
            if char in ['+', '*']:
                operator = char
                break
        
        if numbers and operator:
            problems.append((numbers, operator))
    
    return problems


def part2(data):
    """Solve all problems reading right-to-left (column-based) and return the grand total."""
    problems = parse_input_rtl(data)
    
    grand_total = 0
    for numbers, operator in problems:
        answer = solve_problem(numbers, operator)
        grand_total += answer
    
    return grand_total


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
