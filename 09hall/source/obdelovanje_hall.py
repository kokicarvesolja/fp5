#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import cmasher as cmr
from scipy.optimize import curve_fit
import pandas as pd
import uncertainties.unumpy as unp

# constants
E_g = 0.66 # eV
E_d = 0.01 # eV

# the width of semi-conductor
c = 0.95e-3  # m
# magnetic field
B = 0.173 #T
# Boltzmann's constant
k = 1.38e-23
e_0 = 1.6e-19

# colors

c1, c3, c2 = cmr.take_cmap_colors('cmr.savanna', 3, cmap_range=(.3, .8),
                              return_fmt='hex')

# linearna funkcija za regresijo

def linear(x, k, n):
    return k * x + n


# importing data

data = np.array(pd.read_csv('../meritve/hall.csv', delimiter=','))

dolz_seznama = len(data[:, 1])
# temperature
T = unp.uarray(data[:, 0], dolz_seznama * [1])

# tok
I = unp.uarray(data[:, 1], dolz_seznama * [0.001])
# samo ena vrednost toka, ker je bila napetost prebrana pri tej vrednosti
# napetosti

U1 = unp.uarray(data[:, 2], dolz_seznama * [0.0001])
U2 = unp.uarray(data[:, 3], dolz_seznama * [0.0001])

# plotting R(T)

fig, (ax1, ax2) = plt.subplots(1, 2)

R1 = - U1 / I
R2 = - U2 / I

ax1.plot(unp.nominal_values(T), unp.nominal_values(R1), color=c1, label=r"$R_1 = \frac{U_1}{I_1}$")
ax1.set_title(r"$R_1 (T)$")
ax1.set_xlabel(r"$T [^{\circ} \mathrm{C}]$")
ax1.set_ylabel(r"$R [\Omega]$")
ax1.legend()

ax2.plot(unp.nominal_values(T), unp.nominal_values(R2), color=c2, label=r"$R_2 = \frac{U_2}{I_2}$")
ax2.set_title(r"$R_2 (T)$")
ax2.set_xlabel(r"$T [^{\circ} \mathrm{C}]$")
ax2.set_ylabel(r"$R [\Omega]$")
ax2.legend()

fig.tight_layout()
fig.savefig('../porocilo/figures/r_od_T.png')

plt.close()
# plotting Hall's constant R_H (T)

# fitting the curve
U = - 0.5 * (U2 - U1)
# getting the real current (look at the instructions to the experiment)
# the 70 degree part is wack
hallsConstant = U * c / (I * B)

fitpar, fitcov = curve_fit(linear, unp.nominal_values(T),
                           unp.nominal_values(hallsConstant))

#plottanje in fittanje
plt.errorbar(unp.nominal_values(T), unp.nominal_values(hallsConstant),
             xerr=unp.std_devs(T), yerr=unp.std_devs(hallsConstant),
             color=c1, ms=3, ls='None', marker='o', capsize=2, label='Data')

plt.plot(unp.nominal_values(T), linear(unp.nominal_values(T), *fitpar),
         color=c2, label='Regresija')

# miscs
plt.xlabel(r" $T [^{\circ} \mathrm{C}]$")
plt.ylabel(r" $R_H [ \frac{\mathrm{m}^3}{\mathrm{As}}]$")
plt.title(r"Hallova konstanta $R_H$ v odvisnosti od temperature")

fittext= "Linear fit: $y = kx + n$\nk = {} ± {}\nn = {} ± {}".format(format(fitpar[0], ".4e"),
                                                                     format(fitcov[0][0]**0.5, ".4e"),
                                                                     format(fitpar[1], ".4e"),
                                                                     format(fitcov[1][1]**0.5, ".4e"))
plt.text(16.5, 0.0, fittext, ha='left', va='center', size=10, bbox=dict(facecolor=c3,
                                                                      alpha=0.5))
plt.legend()
plt.savefig('../porocilo/figures/hallovaKonstanta.png')
plt.close()

# --- ln(n_p) (1 / kT) ---

# transforming Celsius to Kelvin

tKelvin = unp.nominal_values(T) + 273

# inverting numpy arrays because ¯\_(ツ)_/¯
xdata = 1 / ((k * tKelvin) / np.abs(e_0))
xdata = xdata[::-1]

ydata = - (unp.nominal_values(I) * B) / (unp.nominal_values(U) * c * e_0)
ydata = ydata[::-1]

# limiting arrays for E_G

eg_xdata = xdata[2:6]
eg_ydata = ydata[2:6]

fitparEg, fitcovEg = curve_fit(linear, eg_xdata, np.log(np.abs(eg_ydata)))
fitEg = linear(xdata, *fitparEg)

print("Printing E_G: ", 2* unp.uarray(fitparEg[0], np.sqrt(np.diag(fitcovEg))[0]))

# limiting arrays for E_D

ed_xdata = xdata[6:]
ed_ydata = ydata[6:]

fitparEd, fitcovEd = curve_fit(linear, ed_xdata, np.log(np.abs(ed_ydata)))
fitEd = linear(xdata, *fitparEd)

print("Printing E_D: ", 2 * unp.uarray(fitparEd[0], np.sqrt(np.diag(fitcovEd))[0]))
# plotting fits

plt.plot(xdata, fitEd, color=c2, label=r"Regresija $E_D$", ls='--', alpha=0.8)
plt.plot(xdata, fitEg, color=c3, label=r"Regresija $E_G$", ls='--', alpha=0.8)

# plotting actual data

plt.plot(xdata, np.log(np.abs(ydata)), color=c1, label='Data', marker='o')

# text data
edfittext= "Linear fit 1: $y_1 = k_1x + n_1$\n$k_1$ = {} ± {}\n$n_1$ = {} ± {}".format(format(fitparEd[0], ".4e"),
                                                                                       format(fitcovEd[0][0]**0.5, ".4e"),
                                                                                       format(fitparEd[1], ".4e"),
                                                                                       format(fitcovEd[1][1]**0.5, ".4e"))
plt.text(36, 57, edfittext, ha="left", va="center", size=10,
         bbox=dict(facecolor=c2, alpha=0.5))
egfittext= "Linear fit 2: $y_2 = k_2x + n_2$\n$k_2$ = {} ± {}\n$n_2$ = {} ± {}".format(format(fitparEg[0], ".4e"),
                                                                                       format(fitcovEg[0][0]**0.5, ".4e"),
                                                                                       format(fitparEg[1], ".4e"),
                                                                                       format(fitcovEg[1][1]**0.5, ".4e"))
plt.text(36, 56, egfittext, ha="left", va="center", size=10,
         bbox=dict(facecolor=c3, alpha=0.5))
plt.title(r"$\ln{n}$ v odvisnosti od $\frac{1}{k_B T}$")
plt.xlabel(r"$(\mathrm{eV})^{-1}$")
plt.ylabel(r"$\ln{n}$")

# miscs

plt.legend()
plt.savefig('../porocilo/figures/logaritemgraf.png')
