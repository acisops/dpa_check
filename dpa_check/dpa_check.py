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

    def custom_prediction_plots(self, plots):
        plots[self.name]['ax'].axhline(self.zero_feps_limit, linestyle='--',
                                       color='dodgerblue', linewidth=2.0)

    def custom_prediction_viols(self, times, temp, viols, load_start):
        """
        Custom handling of limit violations. 

        Parameters
        ----------
        times : NumPy array
            The times for the predicted temperatures
        temp : NumPy array
            The predicted temperatures
        viols : dict
            Dictionary of violations information to add to
        load_start : float
            The start time of the load, used so that we only report
            violations for times later than this time for the model
            run.
        """
        # Only check this violation when all FEPs are off
        mask = self.predict_model.comp['fep_count'].dvals == 0
        zf_viols = self._make_prediction_viols(times, temp, load_start,
                                               self.zero_feps_limit,
                                               "zero-feps", "min",
                                               mask=mask)
        viols["zero_feps"] = {"name": f"Zero FEPs ({self.zero_feps_limit} C)",
                              "type": "Min",
                              "values": zf_viols}

    def custom_validation_plots(self, plots):
        plots[0]['lines']['ax'].axhline(self.zero_feps_limit, linestyle='--',
                                        color='dodgerblue', zorder=-8, 
                                        linewidth=2)

    def _calc_model_supp(self, model, state_times, states, ephem, state0):
        """
        Update to initialize the dpa0 pseudo-node. If 1dpamzt
        has an initial value (T_dpa) - which it does at
        prediction time (gets it from state0), then T_dpa0 
        is set to that.  If we are running the validation,
        T_dpa is set to None so we use the dvals in model.comp

        NOTE: If you change the name of the dpa0 pseudo node you
              have to edit the new name into the if statement
              below.
        """
        if 'dpa0' in model.comp:
            if state0 is None:
                T_dpa0 = model.comp["1dpamzt"].dvals
            else:
                T_dpa0 = state0["1dpamzt"]
            model.comp['dpa0'].set_data(T_dpa0, model.times)


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