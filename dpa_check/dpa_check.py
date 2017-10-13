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

import numpy as np
import xija
import sys
from acis_thermal_check import \
    ACISThermalCheck, \
    calc_off_nom_rolls, \
    get_options, \
    state_builders, \
    get_acis_limits
import os

model_path = os.path.abspath(os.path.dirname(__file__))

yellow_hi, red_hi = get_acis_limits("1dpamzt")

MSID = dict(dpa='1DPAMZT')
# This is the Yellow High IPCL limit.
# 05/2014 - changed from 35.0 to 37.5
YELLOW = dict(dpa=yellow_hi)
# This is the difference between the Yellow High IPCL limit and 
# the Planning Limit. So the Planning Limit is YELLOW - MARGIN
#
# 12/5/13 - This value was changed from 2.5 to 2.0 to reflect the new 
# 1DPAMZT planning limit of 33 degrees C
# 05/19/14 this is changed from 2.0, to 3.0.  2 degress for the normal
#          padding for model error and an additional degree because
#          the total change is being done in increments. We will back
#          this off from 3 degrees to two after a few months trial 
#          testing.  So for now the planning limit will be 34.5 deg. C.
# 09/19/14 - Set MARGIN to 2.0 so that the Planning Limit is now 
#            35.5 deg. C
MARGIN = dict(dpa=2.0)
# 12/5/13 - Likewise the 1DPAMZT validation limits were reduced to 2.0 
#           from 2.5 for the 1% and 99% quantiles
VALIDATION_LIMITS = {'1DPAMZT': [(1, 2.0),
                                 (50, 1.0),
                                 (99, 2.0)],
                     'PITCH': [(1, 3.0),
                                  (99, 3.0)],
                     'TSCPOS': [(1, 2.5),
                                (99, 2.5)]
                     }
HIST_LIMIT = [20.]

def calc_model(model_spec, states, start, stop, T_dpa=None, T_dpa_times=None):
    model = xija.ThermalModel('dpa', start=start, stop=stop,
                              model_spec=model_spec)
    times = np.array([states['tstart'], states['tstop']])
    model.comp['sim_z'].set_data(states['simpos'], times)
    model.comp['eclipse'].set_data(False)
    model.comp['1dpamzt'].set_data(T_dpa, T_dpa_times)
    model.comp['roll'].set_data(calc_off_nom_rolls(states), times)
    for name in ('ccd_count', 'fep_count', 'vid_board', 'clocking', 'pitch'):
        model.comp[name].set_data(states[name], times)

    model.make()
    model.calc()
    return model

def main():
    args = get_options("1DPAMZT", "dpa", model_path)
    dpa_check = ACISThermalCheck("1dpamzt", "dpa",
                                 state_builders[args.state_builder], MSID,
                                 YELLOW, MARGIN, VALIDATION_LIMITS,
                                 HIST_LIMIT, calc_model)
    try:
        dpa_check.driver(args)
    except Exception as msg:
        if args.traceback:
            raise
        else:
            print("ERROR:", msg)
            sys.exit(1)

if __name__ == '__main__':
    main()
