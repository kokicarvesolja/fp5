#!/usr/bin/env python3

import numpy as np
from uncertainties import unumpy as unp
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

def linear(x, k, n):
    return k * x + n

# sorazmernost odziva z modulacijo

data = pd.read_csv(r'./meritve/20Hz.csv')


# napaka

u = np.array(data['U'])
x = unp.uarray(data['X'], [53* 0.01e-3])
y = unp.uarray(data['Y'], [53 * 0.01e-3])

print(unp.nominal_values(x))
# fittanje

fitpar1, fitcov1 = curve_fit(linear, u, unp.nominal_values(x))

fit1 = linear(u, *fitpar1)

fig, ax = plt.subplots()

plt.errorbar(u, unp.nominal_values(x), yerr= unp.std_devs(x),
             markersize=2, ls='None', marker='o', label=r'$\psi_r$')
plt.plot(u, fit1, label='fit')
fittext= "Linear fit: $y = kx + n$\n$k$ =  {} ± {}\n$n$ = {} ± {}"\
    .format(format(fitpar1[0], ".4e"), format(fitcov1[0][0]**0.5, ".4e"),
            format(fitpar1[1], ".4e"), format(fitcov1[1][1]**0.5, ".4e"))
plt.text(0.54, 0.15, fittext, ha="left", va="bottom", size=10, transform=ax.transAxes,
         bbox=dict(facecolor='b', alpha=0.5))
plt.legend()
plt.title("Sorazmernost odziva z modulacijo")
plt.xlabel(r'$U_s[\mathrm{V}]$')
plt.ylabel(r'$\psi [\mathrm{V}]$')
plt.savefig('modulacija.pdf')


# ---- Second part ----
