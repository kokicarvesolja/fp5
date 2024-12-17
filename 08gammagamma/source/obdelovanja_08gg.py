#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cmasher as cmr
from uncertainties import unumpy as unp
import pandas as pd

# all the colors

# colors used
c1, c2, c3 =  cmr.take_cmap_colors('cmr.cosmic', 3, cmap_range=(.5, 1.),
                                   return_fmt='hex')

# --- časovna ločljivost ---

dataCasLoc = np.loadtxt('../meritve/casovna_locljivost_data.txt')

plt.bar(dataCasLoc[:, 0], dataCasLoc[:, 1], width=0.005, color=c1)

# omejitev x osi za lepši, more concise graf
plt.xlim(-0.1, 0.1)

plt.xlabel(r'$t [\mathrm{ns}]$')
plt.ylabel(r'$N$')
plt.title('Časovna ločljivost TDC')
plt.savefig('../porocilo/figures/casovna_locljivost.png')
plt.close()
