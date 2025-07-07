#!/usr/bin/env python3

import argparse
import random

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        'rows',
        type=int
    )
    parser.add_argument(
        'columns',
        type=int
    )
    parser.add_argument(
        'p',
        type=float
    )

    args = parser.parse_args()

    runs = 100000
    filled_col = 0
    for _ in range(runs):
        grid = [[random.random() < args.p for _ in range(args.rows)] for _ in range(args.columns)]

        if any(all(col) for col in grid):
            filled_col += 1

    print(filled_col / runs)


if __name__ == '__main__':
    main()
