#!/usr/bin/env python

"""
Compute and plot the maximum 1DPAMZT settling temperature at any pitch as a
function of time.
"""

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from Ska.Matplotlib import plot_cxctime

import json
import xija
from Chandra.Time import DateTime


def calc_model(start, pitch, n_ccd=6, model_spec='dpa_model_spec.json'):
    stop = DateTime(start) + 4
    model = xija.ThermalModel('dpa', start=start, stop=stop,
                              model_spec=model_spec)

    model.comp['sim_z'].set_data(75000.)
    model.comp['eclipse'].set_data(False)
    model.comp['1dpamzt'].set_data(5)
    model.comp['pitch'].set_data(pitch)
    model.comp['ccd_count'].set_data(n_ccd)
    model.comp['fep_count'].set_data(n_ccd)
    model.comp['clocking'].set_data(1)
    model.comp['vid_board'].set_data(1)
    model.comp['dpa_power'].set_data(0.0)

    model.make()
    model.calc()
    return model


def main():
    plt.figure()
    plt.clf()
    pitchs = range(110, 170, 2)  # only consider tail sun for this plot
    model_spec = json.load(open('dpa_model_spec.json', 'r'))

    colors = {5: 'r', 6: 'b'}
    for n_ccd in range(5, 7):
        settle_temps = []
        times = DateTime(np.arange(2012, 2015, 0.1), format='frac_year').secs
        for tstart in times:
            pitch_temps = []
            for pitch in pitchs:
                model = calc_model(tstart, pitch, n_ccd, model_spec)
                pitch_temps.append(model.comp['1dpamzt'].mvals[-1])
            settle_temp = np.max(pitch_temps)
            settle_temps.append(settle_temp)
            print n_ccd, DateTime(tstart).date, settle_temp

        plot_cxctime(times, settle_temps, label='CCDs={}'.format(n_ccd),
                     color=colors[n_ccd])

    x0, x1 = plt.xlim()
    plt.plot([x0, x1], [32.5, 32.5], '--b')
    plt.plot([x0, x1], [35, 35], '--g')
    plt.plot([x0, x1], [40, 40], '--r')
    plt.ylabel('1DPAMZT (degC)')
    plt.title('Max 1DPAMZT at any pitch')
    plt.grid()
    plt.tight_layout()
    plt.legend(loc='best')
    plt.savefig('max_settling_temp.png')

if __name__ == '__main__':
    main()
