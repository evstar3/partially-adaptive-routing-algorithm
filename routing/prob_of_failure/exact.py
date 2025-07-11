#!/usr/bin/env python3

import argparse
from collections import defaultdict
from mpmath import mp, mpf, nstr

def main():

    mp.dps = 50

    link_probs = [0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.3]
    sizes = [2, 4, 8, 16]

    def regular_system_prob(link_prob, size):
        p_link_good = 1 - link_prob

        p_all_links_good = mp.power(1 - link_prob, size * size)

        p_system_bad = 1 - p_all_links_good
        return p_system_bad

    def my_system_prob(link_prob, size):
        p_row_bad = mp.power(link_prob, size)

        p_row_good = 1 - p_row_bad

        p_system_good = mp.power(p_row_good, size)

        p_system_bad = 1 - p_system_good
        return p_system_bad

    for size in sizes:
        for link_prob in link_probs:
            reg = regular_system_prob(link_prob, size)
            mine = my_system_prob(link_prob, size)
            print(f'{size:.2f} {link_prob:.3f} {nstr(reg, n=6)} -> {nstr(mine, n=6)} ({nstr(reg / mine, n=3)}x)')
        print()

if __name__ == '__main__':
    main()
