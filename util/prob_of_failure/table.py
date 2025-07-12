#!/usr/bin/env python3

import exact
from mpmath import nstr

sizes = [
    (2, 2, 2),
    (4, 4, 2),
    (8, 8, 2),
    (4, 4, 4),
    (8, 8, 4)
]

pzs = [0.0000001, 0.000001, 0.00001, 0.0001, 0.001, 0.01, 0.1, 0.3]

# Relative risk reduction
for x, y, z in sizes:
    for pz in pzs:
        p_reg = exact.p_sys_fail_regular(x, y, z, pz)
        p_adp = exact.p_sys_fail_adaptive(x, y, z, pz)

        rrr = (p_reg - p_adp) / p_reg
        print(nstr(rrr, n=6), end=',')
    print()

# Parts per million saved
for x, y, z in sizes:
    for pz in pzs:
        p_reg = exact.p_sys_fail_regular(x, y, z, pz)
        p_adp = exact.p_sys_fail_adaptive(x, y, z, pz)

        ppm_saved = int((p_reg - p_adp) * 1000000)
        print(ppm_saved, end=',')
    print()

