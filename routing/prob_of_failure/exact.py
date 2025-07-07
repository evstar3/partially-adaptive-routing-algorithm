#!/usr/bin/env python3

import argparse

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

    print(1 - pow(1 - pow(args.p, args.rows), args.columns))

if __name__ == '__main__':
    main()
