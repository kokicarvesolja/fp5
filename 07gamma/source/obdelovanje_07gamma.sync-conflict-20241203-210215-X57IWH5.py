#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cmasher as cmr
from uncertainties import unumpy as unp
import pandas as pd

c1, c2 = cmr.take_cmap_colors('cmr.holly', 2, cmap_range=(.3, .8),
                              return_fmt='hex')

#--- enokanalne meritve ---

data_eno = np.array(pd.read_csv('../meritve/enokanalne.csv',
                                delimiter=';'))

# calculating average and std devs

enokanalne = unp.uarray(np.average(data_eno[:, 1:], axis=1),
                        np.std(data_eno[:, 1:], axis=1))

x_koords = np.arange(0, 8.4, step=0.4)

plt.bar(x_koords, unp.nominal_values(enokanalne), color=c2,
        width=0.4, label='povprečje', zorder=2)
plt.bar(x_koords, (unp.nominal_values(enokanalne) \
                   - unp.std_devs(enokanalne)), color=c1
        , width=0.4, label='deviacija', zorder=3)
plt.bar(x_koords, (unp.nominal_values(enokanalne) \
                   + unp.std_devs(enokanalne)), color=c1,
        alpha=0.5, width=0.4, zorder=1)

plt.xlabel('energija')
plt.ylabel('stevilo delcev')

plt.legend()
plt.title('enokanalni spekter Na')
plt.savefig('../porocilo/figures/enokanalni_na.png')
plt.close()

#--- večkanalne meritve ---

# šum ozadja

data_bg = np.loadtxt('../meriteve/bg.txt')[85:] # real data doesn't start until line 85
time_bg = 657

# aktivnost označena z R
r_bg = data_bg / time_bg
