#!/usr/bin/env python3

import sys
import numpy as np
from types import SimpleNamespace

import scipy

def main():
    names = [
        'fault_rate',
        'num_rows',
        'injection_rate',
        'average_flit_latency',
        'average_packet_latency',
        'flits_receivedtotal',
        'packets_receivedtotal'
    ]

    data = np.genfromtxt(sys.argv[1], skip_header=1, names=names, delimiter=',')

    options = SimpleNamespace()
    options.num_rows = np.unique(data['num_rows'])
    #options.fault_rates = np.unique(data['fault_rate'])
    options.fault_rates = np.array([i / 100 for i in range(0, 16, 1)])
    options.injection_rates = np.unique(data['injection_rate'])

    def do_regression(num_rows, fault_rate):
        config_data = data[np.where((data[np.where(data['num_rows'] == num_rows)])['fault_rate'] == fault_rate)]

        x = config_data['injection_rate']
        y = config_data['average_packet_latency']

        slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
        print(f'{r_value ** 2:.6f}', slope, intercept, num_rows, fault_rate)

    for num_rows in options.num_rows:
        for fault_rate in options.fault_rates:
            do_regression(num_rows, fault_rate)

if __name__ == '__main__':
    main()
