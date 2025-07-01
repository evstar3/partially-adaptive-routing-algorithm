#!/usr/bin/env python3

from pathlib import Path
from collections import defaultdict

import re
import sys

def main():
    configs = set()
    latencies = defaultdict(lambda: defaultdict(list))
    #pattern = re.compile("system.ruby.network.packets_received::total".replace('.', r'\.'))
    pattern = re.compile("system.ruby.network.average_packet_latency".replace('.', r'\.'))

    data_dir = Path(sys.argv[1])
    for path in data_dir.rglob('stats.txt'):
        fault_rate     = float(path.parts[1])
        num_rows       = int(path.parts[2].split('x')[0])
        injection_rate = float(path.parts[3])

        with path.open() as fp:
            lines = fp.readlines()

        for line in lines:
            if re.match(pattern, line):
                configs.add((num_rows, fault_rate))
                latencies[injection_rate][(num_rows, fault_rate)].append(float(line.split()[1]))
                break

    configs_list = list(sorted(configs))

    print(','.join(('injection_rate', *(f'{config[0]}x{config[0]}_{config[1]}' for config in configs_list))))
    for injection_rate, latencies_for_rate in sorted(latencies.items()):
        print(','.join((
            str(injection_rate),
            *(str(sum(latencies_for_rate[config]) / len(latencies_for_rate[config])) if latencies_for_rate[config] else ''
                  for config in configs_list)
        )))

if __name__ == '__main__':
    main()
