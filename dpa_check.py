#!/usr/bin/env python

"""
========================
dpa_check
========================

This code generates backstop load review outputs for checking the ACIS
DPA temperature 1DPAMZT.  It also generates DPA model validation
plots comparing predicted values to telemetry for the previous three weeks.
"""

import sys
import os
import logging
import numpy as np

# Matplotlib setup
# Use Agg backend for command-line (non-interactive) operation
import matplotlib
if __name__ == '__main__':
    matplotlib.use('Agg')

import xija

from model_check import ModelCheck, calc_off_nom_rolls

MSID = dict(dpa='1DPAMZT')

# This is the Yellow High IPCL limit.
# 05/2014 - changed from 35.0 to 37.5
YELLOW = dict(dpa=37.5)

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

TASK_DATA = os.path.dirname(__file__)
logger = logging.getLogger('dpa_check')

_versionfile = os.path.join(os.path.dirname(__file__), 'VERSION')
VERSION = open(_versionfile).read().strip()

def get_options():
    from optparse import OptionParser
    parser = OptionParser()
    parser.set_defaults()
    parser.add_option("--outdir",
                      default="out",
                      help="Output directory")
    parser.add_option("--oflsdir",
                       help="Load products OFLS directory")
    parser.add_option("--model-spec",
                      default=os.path.join(TASK_DATA, 'dpa_model_spec.json'),
                       help="DPA model specification file")
    parser.add_option("--days",
                      type='float',
                      default=21.0,
                      help="Days of validation data (days)")
    parser.add_option("--run-start",
                      help="Reference time to replace run start time "
                           "for regression testing")
    parser.add_option("--traceback",
                      default=True,
                      help='Enable tracebacks')
    parser.add_option("--verbose",
                      type='int',
                      default=1,
                      help="Verbosity (0=quiet, 1=normal, 2=debug)")
    parser.add_option("--ccd-count",
                      type='int',
                      default=6,
                      help="Initial number of CCDs (default=6)")
    parser.add_option("--fep-count",
                      type='int',
                      default=6,
                      help="Initial number of FEPs (default=6)")
    parser.add_option("--vid-board",
                      type='int',
                      default=1,
                      help="Initial state of ACIS vid_board (default=1)")
    parser.add_option("--clocking",
                      type='int',
                      default=1,
                      help="Initial state of ACIS clocking (default=1)")
    parser.add_option("--simpos",
                      default=75616,
                      type='float',
                      help="Starting SIM-Z position (steps)")
    parser.add_option("--pitch",
                      default=150.0,
                      type='float',
                      help="Starting pitch (deg)")
    parser.add_option("--T-dpa",
                      type='float',
                      help="Starting 1DPAMZT temperature (degC)")
    parser.add_option("--version",
                      action='store_true',
                      help="Print version")

    opt, args = parser.parse_args()
    return opt, args

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

if __name__ == '__main__':
    opt, args = get_options()
    if opt.version:
        print VERSION
        sys.exit(0)

    try:
        dpa_check = ModelCheck("1dpamzt", "dpa", MSID,
                               YELLOW, MARGIN, VALIDATION_LIMITS,
                               HIST_LIMIT, calc_model, VERSION)
        dpa_check.driver(opt)
    except Exception, msg:
        if opt.traceback:
            raise
        else:
            print "ERROR:", msg
            sys.exit(1)
