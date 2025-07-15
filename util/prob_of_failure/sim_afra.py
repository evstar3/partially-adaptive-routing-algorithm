#!/usr/bin/env python3

import argparse
import random
from exact import p_fail_afra

def afra_faulty(grid):
    return any(all(any(stack) for stack in plane) for plane in grid)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    parser.add_argument('z', type=int)
    parser.add_argument('pz', type=float)

    args = parser.parse_args()
    x, y, z, pz = args.x, args.y, args.z, args.pz

    runs = 1000000
    count = 0

    for _ in range(runs):
        grid = [[[random.random() < pz for layer in range(z - 1)] for col in range(x)] for row in range(y)]

        if afra_faulty(grid):
            count += 1

    print("Sim:  ", count / runs)
    print("Exact:", p_fail_afra(x, y, z, pz))

if __name__ == '__main__':
    main()
