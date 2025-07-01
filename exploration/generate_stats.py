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

TRAFFIC = ['uniform_random', 'shuffle']
FAULT_RATES = [i / 100 for i in range(0, 16, 1)]
NUM_ROWS = [4, 8]
INJECTION_RATES = [i / 1000 for i in range(20, 301, 10)]
RUNS = 5

GEM5_EXE = Path('../gem5/build/NULL/gem5.debug')
CONFIG = Path('../gem5/configs/example/faulty_garnet_synth_traffic.py')

def get_resultdir(traffic, fault_rate, num_rows, injection_rate, run):
    return Path(traffic, str(fault_rate), f'{num_rows}x{num_rows}', str(injection_rate), str(run))

def run_job(traffic, fault_rate, num_rows, injection_rate, run):
    resultdir = get_resultdir(traffic, fault_rate, num_rows, injection_rate, run)

    with TemporaryDirectory() as rundir:
        print(f'[ START ] {resultdir}', flush=True)
        starttime = time()
        subprocess.run([
            GEM5_EXE,
            f'--outdir={rundir}',
            '--redirect-stdout',
            '--redirect-stderr',
            '--silent-redirect',
            CONFIG,
            '--network=garnet',
            '--sim-cycles=1000000',
            '--topology=FaultyMesh_ZXY',
            f'--synthetic={traffic}',
            f'--fault-rate={fault_rate}',
            f'--mesh-rows={num_rows}',
            f'--num-cpus={num_rows * num_rows}',
            f'--num-dirs={num_rows * num_rows}',
            f'--injectionrate={injection_rate}',
        ])
        endtime = time()

        tempdir = TemporaryDirectory()
        files_to_copy = (
            'config.system.ruby.dot',
            'simerr.txt',
            'simout.txt',
            'stats.txt'
        )

        for file in files_to_copy:
            shutil.copyfile(Path(rundir, file), Path(tempdir.name, file))

        if not resultdir.parent.exists():
            resultdir.parent.mkdir(parents=True)


        shutil.move(tempdir.name, resultdir)
        print(f'[ DONE ] {resultdir} {endtime - starttime:.3f}s', flush=True)

def main():
    assert GEM5_EXE.exists()
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
        for config_info in product(TRAFFIC, FAULT_RATES, NUM_ROWS, INJECTION_RATES, range(1, RUNS+1)):
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
        pool.starmap(run_job, configs())

    print('[ COMPLETE ]')

if __name__ == '__main__':
    main()
