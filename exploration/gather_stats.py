#!/usr/bin/env python3

from pathlib import Path
from collections import OrderedDict

import re
import sys

class Config():
    StatNames = (
        #"simFreq",
        #"simTicks",
        #"system.ruby.clk_domain.clock",
        "system.ruby.network.average_flit_latency",
        #"system.ruby.network.average_flit_network_latency",
        #"system.ruby.network.average_flit_queueing_latency",
        #"system.ruby.network.average_hops",
        "system.ruby.network.average_packet_latency",
        #"system.ruby.network.average_packet_network_latency",
        #"system.ruby.network.average_packet_queueing_latency",
        #"system.ruby.network.avg_link_utilization",
        #"system.ruby.network.avg_vc_load::total",
        #"system.ruby.network.flits_injected::total",
        "system.ruby.network.flits_received::total",
        #"system.ruby.network.int_link_utilization",
        #"system.ruby.network.packets_injected::total",
        "system.ruby.network.packets_received::total",
    )

    def __init__(self, stat_path):
        self.fault_rate     = float(stat_path.parts[1])
        self.num_rows       = int(stat_path.parts[2].split('x')[0])
        self.injection_rate = float(stat_path.parts[3])

        with stat_path.open() as fp:
            lines = fp.readlines()

        stat_names = (name for name in sorted(Config.StatNames))

        self.stats = OrderedDict()

        curr_stat = next(stat_names)
        curr_pattern = re.compile(curr_stat.replace('.', r'\.'))

        for line in sorted(lines):
            if re.match(curr_pattern, line):
                self.stats[curr_stat] = float(line.split()[1])
                try:
                    curr_stat = next(stat_names)
                    curr_pattern = re.compile(curr_stat.replace('.', r'\.'))
                except StopIteration:
                    break

    def csv_header():
        return ','.join(('fault_rate','num_rows','injection_rate',*Config.StatNames))

    def to_csv_string(self):
        return ','.join(
            map(str, [self.fault_rate, self.num_rows, self.injection_rate] + list(self.stats.values()))
        )


def main():
    data = Path(sys.argv[1])

    configs = (Config(path) for path in sorted(data.rglob('stats.txt')))

    print(Config.csv_header())
    for config in configs:
        print(config.to_csv_string())

if __name__ == '__main__':
    main()
