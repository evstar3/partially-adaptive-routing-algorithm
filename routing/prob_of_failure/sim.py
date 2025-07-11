#!/usr/bin/env python3

import argparse
import random

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'size',
        type=int
    )
    parser.add_argument(
        'p',
        type=float
    )

    args = parser.parse_args()

    runs = 1000000
    sys_fail = 0
    for _ in range(runs):
        grid = [[random.random() < args.p for col in range(args.size)] for row in range(args.size)]

        if all(row[0] for row in grid):
            if any(all(row) for row in grid):
                sys_fail += 1

    print(sys_fail / runs)


if __name__ == '__main__':
    main()
