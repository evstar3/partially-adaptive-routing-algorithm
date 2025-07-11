#!/usr/bin/env python3

import argparse
from collections import defaultdict
from mpmath import mp, mpf, nstr

def main():

    mp.dps = 50

    link_probs = [0.001, 0.005, 0.01, 0.05, 0.1, 0.15, 0.3]
    sizes = [2, 4, 8, 16]

    def system_prob(link_prob, size):
        p_row_bad = mp.power(link_prob, size)

        p_row_good = 1 - p_row_bad

        p_system_good = mp.power(p_row_good, size)

        p_system_bad = 1 - p_system_good
        return p_system_bad

    print(
        '\n'.join(
            ','.join(
                nstr(system_prob(link_prob, size), n=3, min_fixed=-3, strip_zeros=False)
                for link_prob in link_probs
            )
            for size in sizes
        )
    )
    

if __name__ == '__main__':
    main()
