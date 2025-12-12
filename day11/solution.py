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


def count_paths_with_required(graph, start, end, required):
    """
    Count all paths from start to end that visit all required nodes.
    Uses DP with memoization - state is (node, bitmask of visited required nodes).
    Since data only flows forward (DAG), we don't need to track full visited set.
    """
    from functools import lru_cache
    
    required_list = list(required)
    required_to_bit = {node: 1 << i for i, node in enumerate(required_list)}
    full_mask = (1 << len(required_list)) - 1
    
    @lru_cache(maxsize=None)
    def dp(node, mask):
        """Count paths from node to end with given required-nodes mask."""
        # Update mask if we're at a required node
        if node in required_to_bit:
            mask |= required_to_bit[node]
        
        # If we reached the end, count only if we visited all required nodes
        if node == end:
            return 1 if mask == full_mask else 0
        
        # If this node has no outputs, dead end
        if node not in graph:
            return 0
        
        # Sum paths through all neighbors
        total = 0
        for neighbor in graph[node]:
            total += dp(neighbor, mask)
        
        return total
    
    return dp(start, 0)


def part2(data):
    """Find paths from 'svr' to 'out' that visit both 'dac' and 'fft'."""
    graph = parse_input(data)
    required = {'dac', 'fft'}
    return count_paths_with_required(graph, 'svr', 'out', required)


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
