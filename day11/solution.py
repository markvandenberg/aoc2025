#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 11: Reactor
"""

def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse the device connections into a graph."""
    graph = {}
    lines = data.split('\n')
    
    for line in lines:
        if ':' not in line:
            continue
        
        device, outputs = line.split(':')
        device = device.strip()
        outputs = outputs.strip().split()
        
        graph[device] = outputs
    
    return graph


def count_paths(graph, start, end, visited=None):
    """Count all paths from start to end using DFS."""
    if visited is None:
        visited = set()
    
    # If we reached the end, we found a path
    if start == end:
        return 1
    
    # If this node has no outputs, dead end
    if start not in graph:
        return 0
    
    # Mark current node as visited to avoid cycles
    visited.add(start)
    
    # Count paths through each neighbor
    total_paths = 0
    for neighbor in graph[start]:
        if neighbor not in visited:
            total_paths += count_paths(graph, neighbor, end, visited)
    
    # Unmark node when backtracking (important for finding all paths)
    visited.remove(start)
    
    return total_paths


def part1(data):
    """Find number of paths from 'you' to 'out'."""
    graph = parse_input(data)
    return count_paths(graph, 'you', 'out')


def part2(data):
    """Solve part 2."""
    graph = parse_input(data)
    # TODO: Implement when part 2 is revealed
    return None


def main():
    import sys
    # Read input
    filename = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'
    data = read_input(filename)
    
    # Solve parts
    result1 = part1(data)
    print(f"Part 1: {result1}")
    
    result2 = part2(data)
    if result2 is not None:
        print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
