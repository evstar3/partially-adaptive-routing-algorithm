#!/usr/bin/env python3

import argparse
from mpmath import mp, mpf, nstr

mp.dps = 70

def p_sys_fail_regular(x, y, z, pz):
    return 1 - mp.power(1 - pz, (x * y) * (z - 1))


def p_sys_fail_adaptive(x, y, z, pz):
    return 1 - mp.power(1 - (mp.power(pz, x) * (1 - mp.power(1 - mp.power(pz, x - 1), y))), z - 1)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('x', type=int)
    parser.add_argument('y', type=int)
    parser.add_argument('z', type=int)
    parser.add_argument('pz', type=mpf)

    args = parser.parse_args()
    x, y, z, pz = args.x, args.y, args.z, args.pz

    p_reg = p_sys_fail_regular(x, y, z, pz)
    p_adp = p_sys_fail_adaptive(x, y, z, pz)

    print(nstr(p_reg, n=6))
    print(nstr(p_adp, n=6))
    print(nstr(p_reg / p_adp, n=6))

if __name__ == '__main__':
    main()
