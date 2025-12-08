#!/usr/bin/env python3
"""
Advent of Code 2025 - Day 8: Playground
"""
import heapq
from collections import defaultdict


def read_input(filename='input.txt'):
    """Read and return the input file."""
    with open(filename, 'r') as f:
        return f.read().strip()


def parse_input(data):
    """Parse junction box positions."""
    lines = data.split('\n')
    positions = []
    for line in lines:
        if line.strip():
            x, y, z = map(int, line.split(','))
            positions.append((x, y, z))
    return positions


def distance_sq(p1, p2):
    """Calculate squared Euclidean distance between two 3D points."""
    return ((p1[0] - p2[0]) ** 2 +
            (p1[1] - p2[1]) ** 2 +
            (p1[2] - p2[2]) ** 2)


class UnionFind:
    """Union-Find data structure for tracking connected components."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
    
    def find(self, x):
        """Find root of x with path compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union two components. Returns True if they were not already connected."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
        
        # Union by size
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        return True
    
    def get_component_sizes(self):
        """Get sizes of all connected components."""
        components = defaultdict(int)
        for i in range(len(self.parent)):
            root = self.find(i)
            components[root] = self.size[root]
        return list(components.values())


def iter_edges(positions):
    """Yield all unique edges with their squared distances."""
    n = len(positions)
    for i in range(n):
        for j in range(i + 1, n):
            yield (distance_sq(positions[i], positions[j]), i, j)


def part1(data, num_connections=1000):
    """Connect the closest pairs and find product of three largest circuits."""
    positions = parse_input(data)
    n = len(positions)

    smallest_edges = heapq.nsmallest(num_connections, iter_edges(positions))

    uf = UnionFind(n)
    for _, i, j in smallest_edges:
        uf.union(i, j)

    sizes = uf.get_component_sizes()
    sizes.sort(reverse=True)

    if len(sizes) >= 3:
        return sizes[0] * sizes[1] * sizes[2]
    return 0


def part2(data):
    """Find the last connection needed to form one circuit."""
    positions = parse_input(data)
    n = len(positions)

    edges = sorted(iter_edges(positions))

    uf = UnionFind(n)
    num_components = n
    last_connection = None

    for _, i, j in edges:
        if uf.union(i, j):
            num_components -= 1
            last_connection = (i, j)
            if num_components == 1:
                break

    if last_connection:
        i, j = last_connection
        x1, _, _ = positions[i]
        x2, _, _ = positions[j]
        return x1 * x2

    return 0


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
