#!/usr/bin/env python3

import sys

import pandas as pd
import statsmodels.api as sm

def main():
    data = pd.read_csv(sys.argv[1])

    independent_vars = ['fault_rate', 'num_rows', 'injection_rate']
    dependent_vars = [field for field in data.axes[1] if field not in independent_vars]

    x = data[independent_vars]
    x = sm.add_constant(x)

    for dep_var in dependent_vars:
        y = data[dep_var]
        model = sm.OLS(y, x).fit()
        print(model.summary())



if __name__ == '__main__':
    main()
