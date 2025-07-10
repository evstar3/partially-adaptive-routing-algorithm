#!/usr/bin/env python3

import subprocess
import shutil
import sys

from multiprocessing import Pool
from itertools import product
from pathlib import Path
from tempfile import TemporaryDirectory
from time import time
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

TRAFFIC = ['uniform_random']
FAULT_RATES = [i / 100 for i in range(0, 16, 1)]
SIZES = [(4, 4), (8, 8)] # (row, col)
INJECTION_RATES = [i / 100 for i in range(2, 41, 1)]
RUNS = 10

GEM5_OPT_EXE = Path('../gem5/build/NULL/gem5.opt')
CONFIG = Path('../gem5/configs/example/faulty_garnet_synth_traffic.py')

def get_resultdir(traffic, fault_rate, size, injection_rate, run):
    rows, cols = size
    return Path(traffic, str(fault_rate), f'{rows}x{cols}', str(injection_rate), str(run))

def run_job(config):
    traffic, fault_rate, size, injection_rate, run = config

    resultdir = get_resultdir(traffic, fault_rate, size, injection_rate, run)

    rows, cols = size

    with TemporaryDirectory() as rundir:
        print(f'[ START ] {resultdir}', flush=True)

        starttime = time()
        try:
            subprocess.run([
                GEM5_OPT_EXE,
                f'--outdir={rundir}',
                '--redirect-stdout',
                '--redirect-stderr',
                '--silent-redirect',
                CONFIG,
                '--network=garnet',
                '--sim-cycles=1000000',
                '--topology=FaultyMesh_ZXY',
                '--routing-algorithm=2', # custom
                f'--synthetic={traffic}',
                f'--fault-rate={fault_rate}',
                f'--mesh-rows={rows}',
                f'--mesh-cols={cols}',
                f'--num-cpus={rows * cols}',
                f'--num-dirs={rows * cols}',
                f'--injectionrate={injection_rate}',
            ])
            endtime = time()

            files_to_copy = ('stats.txt',)
            status = 'DONE'
            message = f'{resultdir} {endtime - starttime:.3f}s'

        except subprocess.CalledProcessError as e:
            files_to_copy = (
                'config.system.ruby.dot',
                'simerr.txt',
                'simout.txt',
                'stats.txt'
            )
            status = 'ERROR'
            message = f'{resultdir} {e}'

        tempdir = TemporaryDirectory()

        for file in files_to_copy:
            shutil.copyfile(Path(rundir, file), Path(tempdir.name, file))

        if not resultdir.parent.exists():
            resultdir.parent.mkdir(parents=True)

        shutil.move(tempdir.name, resultdir)

    print(f'[ {status} ] {message}')

def main():
    assert GEM5_OPT_EXE.exists()
    assert CONFIG.exists()

    parser = ArgumentParser(
        formatter_class=ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        '-j', '--jobs',
        type=int,
        default=1,
        help='Number of parallel processes'
    )
    parser.add_argument(
        '-f', '--force',
        action="store_true",
        help='Do not ask for confirmation'
    )

    args = parser.parse_args()

    def configs():
        for config_info in product(TRAFFIC, FAULT_RATES, SIZES, INJECTION_RATES, range(1, RUNS+1)):
            resultdir = get_resultdir(*config_info)

            if resultdir.exists():
                continue

            yield config_info

    jobs = 0
    for config in configs():
        jobs += 1

    print(f'{sys.argv[0]}: need to run {jobs} jobs')
    if (not args.force):
        print(f'{sys.argv[0]}: continue?', end=' ')
        response = input()
        if response.lower() not in ('y', 'yes'):
            sys.exit(0)

    with Pool(processes=args.jobs) as pool:
        for _ in pool.imap_unordered(run_job, configs(), chunksize=64):
            pass

    print('[ COMPLETE ]')

if __name__ == '__main__':
    main()
