#!/usr/bin/env python3

import argparse
import random

def regular_faulty(grid):
    if any((any(row) for row in layer) for layer in grid):
        return True

    return False

def adaptive_faulty(grid):
    def layer_faulty(layer):
        if not all(row[0] for row in layer):
            return False

        if not any(all(row) for row in layer):
            return False

        return True
            
    return any(layer_faulty(layer) for layer in grid)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    parser.add_argument('z', type=int)
    parser.add_argument('pz', type=float)

    args = parser.parse_args()
    x, y, z, pz = args.x, args.y, args.z, args.pz

    runs = 1000000
    regular_count = 0
    adaptive_count = 0


    for _ in range(runs):
        grid = [[[random.random() < pz for col in range(x)] for row in range(y)] for layer in range(z - 1)]

        if regular_faulty(grid):
            regular_count += 1

        if adaptive_faulty(grid):
            adaptive_count += 1

    print(regular_count / runs)
    print(adaptive_count / runs)


if __name__ == '__main__':
    main()
