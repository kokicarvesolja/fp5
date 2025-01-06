#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
from uncertainties import unumpy as unp
from scipy.optimize import curve_fit

# colors

c1, c2, c3, d1, d2, d3 = cmr.take_cmap_colors('cmr.lavender', 6,
                                              cmap_range=(0.3, 1.0),
                                              return_fmt='hex')

# diagonala tuljave
# krajsi polmer
r_1 = unp.uarray([4.5], [0.1]) * 1e-2 # cm
# daljsi polmer
r_2 = unp.uarray([8.7], [0.1]) * 1e-2 # cm
# dolzina tuljave
l = unp.uarray([13.2], [0.1]) * 1e-2 # cm
# vrednost diagonale
d = unp.sqrt(l**2 + (r_1 + r_2)**2)

print("Vrednost diagonale: ", d)

# --- functions I need ---

def linear(x, k, n):
    return k * x + n

def magnetno_polje(I, dolzina=d):
    mi_0 = 4 * 3.14 * 1e-7 # Vs/Am
    N = 1557
    return (N * mi_0 * I) / dolzina

# --- odvod absorpcijskega vrha ---

# definiram funkcijo za obdelovanje podatkov

def abs_crte(nu, I0, color):
    # reading the data
    data = np.array(pd.read_csv(f'../meritve/{nu}MHz.csv', delimiter=','))
    # for uncertainties package to produce STD devs
    lenData = len(data[:, 0])

    tok = unp.uarray(data[:, 0], lenData * [1])
    volt = unp.uarray(data[:, 1], 0.05 * np.abs(data[:, 1]))

    # getting min and max value for \Delta B (look at the definition)

    maxData = np.argmax(unp.nominal_values(volt))
    minData = np.argmin(unp.nominal_values(volt))

    # calculating \Delta B

    deltaI = tok[minData] - tok[maxData] # v mA

    deltaB = magnetno_polje(deltaI) # v mT
    print(f'Vrednost za Delta B pri {nu} v mT: ', deltaB)

    # vrednost B0 pri I0, kar je pri U = 0 med maksimumom in minimumom absorpcijske
    # crte
    # podano kot argument funkciji
    B0 = magnetno_polje(I0)
    print(f'Vrednost B0 pri {nu} MHz v m', B0)

    nuOverB0 = nu/(B0 * 1e-3)
    print(f'Vrednost nu/B0 v GHz / T pri {nu}: ', nuOverB0 * 1e-3)
    # se plot za to vrednost

    plt.errorbar(unp.nominal_values(tok), unp.nominal_values(volt),
                 xerr=unp.std_devs(tok), yerr=unp.std_devs(volt),
                 color=color[0], label=fr'$\nu =$ {nu}' + r'$\mathrm{MHz}$',
                 marker='.', capsize=2, zorder=2)
    # putting it on top
    plt.plot(I0, 0, marker='x', label=r'$I_0$: $U = 0$', color=color[1], zorder=1)

    return B0

frekv = [80, 85, 90]
# I went and guesstimated from measurements, where it crossed the x axis
# for example in 90MHz.csv in line 69 is I = 290 mA and U = 280, and in line
# 70 is I = 291 mA and U =-260
# Also funny number ^-^
tokI0 = [273.75, 290.5, 308.5]

barve = [(d1, c1), (d2, c2), (d3, c3)]

vrednostB0 = np.ones(3)
stdB0 = np.ones(3)

for f, I, b, no in zip(frekv, tokI0, barve, range(0, 3)):
    temp = abs_crte(f, I, b)
    vrednostB0[no] = unp.nominal_values(temp)
    stdB0[no] = unp.std_devs(temp)

B0array = unp.uarray(vrednostB0, stdB0)


# miscs
plt.axhline(alpha=1, ls=":", c="#adadad")
plt.title(r"Odvod absorpcijske črte pri $80, 85, 90$ MHz")
plt.xlabel("I [mA]")
plt.ylabel("U [mV]")
plt.legend()
plt.savefig('../porocilo/figures/abs_crte.png')
plt.close()

# --- g value ---
# finding out the g (spot) value

fitpar, fitcov = curve_fit(linear, frekv, unp.nominal_values(B0array))

fit = linear(np.linspace(80, 90, 100), *fitpar)

plt.errorbar(frekv, unp.nominal_values(B0array), yerr=unp.std_devs(B0array),
             ls='None',
             color=c1, marker='.', capsize=2, label='izracunano')
plt.plot(np.linspace(80, 90, 100), fit, color=d1, label='regresija')

plt.title(r'$B_0$ v odvisnosti od resonančne frekvence $\nu$')
plt.xlabel(r'$\nu [\mathrm{MHz}]$')
plt.ylabel(r'$B_0 [\mathrm{T}]$')
plt.legend()
plt.savefig('../porocilo/figures/gfaktor.png')
plt.close()

# konstante
# Bohrov magneton
mu_B = 9.27e-24
maxwellH = 6.62e-34

naklon = unp.uarray(fitpar[0], np.sqrt(np.diag(fitcov))[0])

# naklon je definiran kot (B1 - B0)/(nu1 - nu0), kar najdemo v g = maxwellH / (mu_B * naklon)

# calculating g

gFaktor = maxwellH / (mu_B * naklon)

print(gFaktor)
