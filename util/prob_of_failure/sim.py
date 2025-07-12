#!/usr/bin/env python3

import argparse
import random

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
        grid = [[[random.random() < pz for col in range(y)] for row in range(x)] for layer in range(z - 1)]

        if any((any(row) for row in layer) for layer in grid):
            regular_count += 1

        for layer in grid:
            if all(row[0] for row in layer) and any(all(row) for row in layer):
                adaptive_count += 1
                break

    print(regular_count / runs)
    print(adaptive_count / runs)


if __name__ == '__main__':
    main()
