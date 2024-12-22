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

# functions needed

def linear(x, k, n):
    return k * x + n

# for eliminating zero and negative values

def masking(x, y):
    mask = x > 0
    return x[mask], y[mask]

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

# --- radioaktivni razpad ---

dataRadRaz = np.loadtxt('../meritve/radioaktivni_razpad_data.txt')
casMerjenjaRadRaz = 31.6

# Graf radioaktivnih razpadov

plt.bar(dataRadRaz[:, 0], dataRadRaz[:, 1] / casMerjenjaRadRaz, width=0.005, color=c1)

plt.xlabel(r'$t [\mathrm{ns}]$')
plt.ylabel(r'$R [\mathrm{ns}^{-1}]$')
plt.title(r'Radioaktivni razpad $^{22} \mathrm{Na}$ ')
plt.savefig('../porocilo/figures/radio_razpad.png')
plt.close()

# Logaritmiran graf radioaktivnih razpadov

casMeritve = 31.6 # sekund

casRadRaz = dataRadRaz[:, 0] / 1e9
meritveRadRaz = dataRadRaz[:, 1] / casMeritve # delim s casom zato, da dobim aktivnost

novRadRaz, novCasRadRaz = masking(meritveRadRaz, casRadRaz)

fitparRadRaz, fitcovRadRaz = curve_fit(linear, novCasRadRaz, np.log(novRadRaz))

napake = np.sqrt(np.diag(fitcovRadRaz))

# plotting fit
# Upoštevam Markov nasvet in naredim osi bolj goste za lepši graf

abscisa = np.linspace(0, novCasRadRaz[-1], num=10000)
ordinataRadRaz = linear(abscisa, *fitparRadRaz)

plt.plot(abscisa, ordinataRadRaz, color=c2)
plt.scatter(novCasRadRaz, np.log(novRadRaz), color=c1, s=3)

fittext= "Linear fit 1: $y = kx + n$\n$k_1$ = {} ± {}\n$n_1$ = {} ± {}".format(format(fitparRadRaz[0], ".2e"),
                                                                               format(napake[0], ".2e"),
                                                                               format(fitparRadRaz[1], ".2e"),
                                                                               format(napake[1], ".2e"))

plt.text(8.0, 3.0, fittext, ha='left', va='center', size=10,
         bbox=dict(facecolor=c3, alpha=0.5))

plt.title(r'Lineariziran graf radioaktivnega razpada $^{22} \mathrm{Na}$')
plt.xlabel(r'$t [\mathrm{ms}]$')
plt.ylabel(r'$ \ln \left( \frac{\Delta p}{\Delta t} \right)$')
plt.savefig('../porocilo/figures/log_radio_razpad.png')
plt.close()
