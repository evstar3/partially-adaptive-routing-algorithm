#!/usr/bin/env python3

import argparse
from collections import defaultdict
from mpmath import mp, mpf, nstr

mp.dps = 70

def regular_system_prob(p_link_bad, size):
    p_link_good = 1 - p_link_bad

    p_all_links_good = mp.power(1 - p_link_bad, size * size)

    p_system_bad = 1 - p_all_links_good
    return p_system_bad

def route0_system_prob(p_link_bad, size):
    p_row_bad = mp.power(p_link_bad, size)

    p_row_good = 1 - p_row_bad

    p_system_good = mp.power(p_row_good, size)

    p_system_bad = 1 - p_system_good
    return p_system_bad

def route1_system_prob(p_link_bad, size):
    p_first_col_bad = mp.power(p_link_bad, size)

    p_row_bad_given_first_col_bad = mp.power(p_link_bad, size - 1)

    p_row_good_given_first_col_bad = 1 - p_row_bad_given_first_col_bad

    p_all_rows_good_given_first_col_bad = mp.power(p_row_good_given_first_col_bad, size)

    p_any_row_bad_given_first_col_bad = 1 - p_all_rows_good_given_first_col_bad

    p_system_bad = p_first_col_bad * p_any_row_bad_given_first_col_bad

    return p_system_bad

def main():
    link_probs = [0.00001, 0.0001, 0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.3]
    sizes = [2, 4, 8, 16]

    for size in sizes:
        for link_prob in link_probs:
            reg = regular_system_prob(link_prob, size)
            route0 = route0_system_prob(link_prob, size)
            route1 = route1_system_prob(link_prob, size)
            print(f'{size}x{size}, p_link_fail={link_prob}')
            print(f'    regular routing: {nstr(reg, n=6)}')
            print(f'            x sweep: {nstr(route0, n=6)}')
            print(f'      x and y sweep: {nstr(route1, n=6)}')
            print()

        print()

if __name__ == '__main__':
    main()
