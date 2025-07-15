#!/usr/bin/env python3

import argparse
import random
from exact import p_fail_ftzoe

def ft_faulty(grid):
    for layer in grid:
        if layer[0][0] and layer[0][1]:
            return True

        if layer[0][0] and layer[1][0]:
            return True

    return False

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
        grid = [[[random.random() < pz for col in range(y)] for row in range(x)] for layer in range(z - 1)]

        if ft_faulty(grid):
            count += 1

    print("Sim:  ", count / runs)
    print("Exact:", p_fail_ftzoe(x, y, z, pz))

if __name__ == '__main__':
    main()
