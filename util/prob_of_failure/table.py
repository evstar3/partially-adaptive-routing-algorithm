#!/usr/bin/env python3

import exact
from mpmath import nstr
from itertools import product

algs = {
    'DOR': exact.p_fail_regular,
    'FT-Z-OE': exact.p_fail_ftzoe,
    'AFRA': exact.p_fail_afra,
    'This work': exact.p_fail_adaptive
}

sizes = (
    (2, 2, 2),
    (4, 4, 2),
    (8, 8, 2),
    (4, 4, 4),
    (8, 8, 4),
    (8, 8, 8),
)

pzs = (0.001, 0.01, 0.1, 0.3)

print(f'''& {' & '.join(map(str, pzs))} \\cr''')
for x, y, z in sizes:
    print(f'{x}x{y}x{z} \\cr')
    for name, func in algs.items():
        print(f'{name}', end=' & ')
        print(' & '.join(nstr(func(x, y, z, pz), n=3) for pz in pzs), end='')
        print(' \\cr')



