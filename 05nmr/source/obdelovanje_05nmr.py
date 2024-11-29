#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from uncertainties import unumpy
import cmasher as cmr

c1, c2 = cmr.take_cmap_colors('cmr.arctic', 2, cmap_range=(0.5, .8),
                              return_fmt='hex')

def linearna(x, k, n):
    return x * k + n

data_precesija = np.array(pd.read_csv('../meritve/prosta_precesija_2.csv',
                                      delimiter=','))

cas = data_precesija[:, 0]
napetost = np.log(data_precesija[:, 1])

# omejitev podatkov na cas manj kot 500

napetost = napetost[500 > cas]
cas = cas[500 > cas]

fitpar, fitcov = curve_fit(linearna, cas, napetost)
print(fitpar, np.sqrt(np.diag(fitcov)))

plt.scatter(cas, napetost, color=c1, label='meritve', marker='.')
plt.plot(cas, linearna(cas, *fitpar), ls='--', color=c2,
         label='fit')

plt.xlabel(r'Čas $t [\mathrm{ms}]$')
plt.ylabel(r'Amplituda $U[\mathrm{V}]$')

plt.legend()
plt.title(r'Izračunavanje časa $T_2^{*}$')
plt.savefig('../porocilo/figures/cas_t2_zvezdica.png')
plt.close()
