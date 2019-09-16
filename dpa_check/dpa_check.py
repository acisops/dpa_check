#!/usr/bin/env python

"""
========================
dpa_check
========================

This code generates backstop load review outputs for checking the ACIS
DPA temperature 1DPAMZT.  It also generates DPA model validation
plots comparing predicted values to telemetry for the previous three
weeks.
"""
from __future__ import print_function

# Matplotlib setup
# Use Agg backend for command-line (non-interactive) operation
import matplotlib
matplotlib.use('Agg')

import sys
from acis_thermal_check import \
    ACISThermalCheck, \
    get_options
import os

model_path = os.path.abspath(os.path.dirname(__file__))


class DPACheck(ACISThermalCheck):
    def __init__(self):
        valid_limits = {'1DPAMZT': [(1, 2.0), (50, 1.0), (99, 2.0)],
                        'PITCH': [(1, 3.0), (99, 3.0)],
                        'TSCPOS': [(1, 2.5), (99, 2.5)]
                        }
        hist_limit = [20.0]
        super(DPACheck, self).__init__("1dpamzt", "dpa", valid_limits,
                                       hist_limit)


def main():
    args = get_options("dpa", model_path)
    dpa_check = DPACheck()
    try:
        dpa_check.run(args)
    except Exception as msg:
        if args.traceback:
            raise
        else:
            print("ERROR:", msg)
            sys.exit(1)


if __name__ == '__main__':
    main()