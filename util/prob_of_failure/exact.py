#!/usr/bin/env python3

import argparse
from mpmath import mp, mpf, nstr

mp.dps = 70

def p_fail_regular(x, y, z, pz):
    return 1 - mp.power(1 - pz, (x * y) * (z - 1))

def p_fail_afra(x, y, z, pz):
    return 1 - mp.power(1 - mp.power(1 - mp.power(1 - pz, z - 1), x), y)

def p_fail_ftzoe(x, y, z, pz):
    p_layer_bad = pz * (1 - mp.power(1 - pz, 2))
    return 1 - mp.power(1 - p_layer_bad, z - 1)

def p_fail_adaptive(x, y, z, pz):
    p_layer_faulty = mp.power(pz, y) * (1 - mp.power(1 - mp.power(pz, x - 1), y))

    return 1 - mp.power(1 - p_layer_faulty, z - 1)
