#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from uncertainties import unumpy as unp
import cmasher as cmr

c1, c2 = cmr.take_cmap_colors('cmr.arctic', 2, cmap_range=(.3, .8),
                              return_fmt='hex')

def linearna(x, k, n):
    return x * k + n

# reading ion water data
# I got data from WebPlotDigitizer, version 4

data_precesija = np.array(pd.read_csv('../meritve/prosta_precesija_2.csv',
                                      delimiter=','))

# I logarithm the values because fitting of exponential curve did
# not have any applicable results
cas = data_precesija[:, 0]
napetost = np.log(data_precesija[:, 1])

# omejitev podatkov na cas manj kot 500 for easier fitting
# data after that ruin the fit because they become flat

napetost = napetost[500 > cas]
cas = cas[500 > cas]

fitpar, fitcov = curve_fit(linearna, cas, napetost)

# čas T2* je definiran kot 1/t, ki sem ga dobil iz grafa
# saj je u0 * e^{t/T2}

t2_star = - 1 / unp.uarray(fitpar[0], np.sqrt(np.diag(fitcov))[0])
print('T2*: ', t2_star)

# I get T2* = 0.269 \pm 0.004 ms
# Podobno oceno dobimo tudi iz širine spinskega odmeva
# Širina je 2 * T2* in pri meni je širina about 540 ms, kar se ujema
# z mojim izračunanim rezultatom

# plotting the data and fit
plt.scatter(cas, napetost, color=c1, label='meritve', marker='.')
plt.plot(cas, linearna(cas, *fitpar), ls='--', color=c2,
         label='fit')

plt.xlabel(r'Čas $t [\mathrm{ms}]$')
plt.ylabel(r'Amplituda $\ln U + \text{konst}[\mathrm{V}]$')

plt.legend()
plt.title(r'Izračunavanje časa $T_2^{*}$')
plt.savefig('../porocilo/figures/cas_t2_zvezdica.png')
plt.close()

# nehomogenost magnetnega polja - ocena

gamma = 2.675e8

delta_B_z = 1 / (gamma * t2_star * 10e-6)

print("Nehomogenost polja: ", delta_B_z)

# --- umeritev skale ---

data_umeritev = np.array(pd.read_csv('../meritve/umeritev.csv',
                                     delimiter=','))

gumb = data_umeritev[:, 0]
zakasnitev = data_umeritev[:, 1]

fitpar_umer, fitpar_cov = curve_fit(linearna, gumb, zakasnitev)

text = 'fit ' + 'k = {:.3f}, '.format(fitpar_umer[0]) \
    + 'n = {:.3f}'.format(fitpar_umer[1])

plt.scatter(gumb, zakasnitev, color=c1, label='meritve', marker='.')
plt.plot(gumb, linearna(gumb, *fitpar_umer), color=c2, label=text)

plt.xlabel(r'Oznaka na gumbu')
plt.ylabel(r'Zakasnitev na osciloskopu $[\mathrm{ms}]$')

plt.legend()
plt.title('Umeritev skale')
plt.savefig('../porocilo/figures/umeritev_skale.png')
plt.close()

# --- spinsko-mrežni relaksacijski čas T1 ---

def eksponentna(x, m0, t1):
    return m0 * (1. - np.exp(-x / t1))
# ion water
data_ion_t1 = np.array(pd.read_csv('../meritve/ion_water_t1.csv',
                                   delimiter=','))

cas_ion_t1 = data_ion_t1[:, 0] * fitpar_umer[0] * 10e-3
napetost_ion_t1= data_ion_t1[:, 1]
# for linear fit
napetost_ion_t1 = np.log(data_ion_t1[:, 1])[cas_ion_t1 < 5]

# adjusting data for linear fit
cas_ion_t1 = cas_ion_t1[cas_ion_t1 < 5]

# for linear fit
#fitpar_t1_ion, fitcov_t1_ion = curve_fit(linearna, cas_ion_t1,
#                                         napetost_ion_t1)

fitpar_t1_ion, fitcov_t1_ion = curve_fit(eksponentna, cas_ion_t1,
                                         napetost_ion_t1)

t1_ion =  1 / unp.uarray(fitpar_t1_ion[1],
                          np.sqrt(np.diag(fitcov_t1_ion))[1])
print("T1 voda z ioni: ", t1_ion)

text1 = 'fit ' + ' m0 = {:.3f}'.format(fitpar_t1_ion[0]) \
    + ' 1/t1 = {:.3f}'.format(fitpar_t1_ion[1])

plt.scatter(cas_ion_t1, napetost_ion_t1, color=c1, label='meritev',
            marker='.')
plt.plot(cas_ion_t1, eksponentna(cas_ion_t1, *fitpar_t1_ion),
         color=c2, label=text1)


plt.xlabel(r'Čas zakasnitve $t[\mathrm{ms}]$')
plt.ylabel(r'Amplituda $[\mathrm{V}]$')

plt.legend()
plt.title('Voda s paramagnetnimi ioni')
plt.savefig('../porocilo/figures/t1_ion.png')
plt.close()


# tap water

data_tap_t1 = np.array(pd.read_csv('../meritve/tap_water_t1.csv',
                                   delimiter=','))

cas_tap_t1 = data_tap_t1[:, 0] * fitpar_umer[0] * 10e-6
napetost_tap_t1 = data_tap_t1[:, 1]

# adjusting data for linear fit
#cas_tap_t1 = cas_tap_t1[cas_tap_t1 > 0.0]

#fitpar_t1_tap, fitcov_t1_tap = curve_fit(linearna, cas_tap_t1,
#                                         napetost_tap_t1)
fitpar_t1_tap, fitcov_t1_tap = curve_fit(eksponentna, cas_tap_t1,
                                         napetost_tap_t1)

t1_tap =  1 / unp.uarray(fitpar_t1_tap[0],
                          np.sqrt(np.diag(fitcov_t1_tap))[0])
print("T1 voda brez ionov: ", t1_tap)

text1 = 'fit ' + ' k = {:.3f}'.format(fitpar_t1_tap[0]) \
    + ' n = {:.3f}'.format(fitpar_t1_tap[1])

plt.scatter(cas_tap_t1, napetost_tap_t1, color=c1, label='meritev',
            marker='.')
plt.plot(cas_tap_t1, eksponentna(cas_tap_t1, *fitpar_t1_tap),
         color=c2, label=text1)


plt.xlabel(r'Čas zakasnitve $t[\mathrm{s}]$')
plt.ylabel(r'Amplituda $[\mathrm{V}]$')

plt.legend()
plt.title('Voda brez paramagnetnih ionov')
plt.savefig('../porocilo/figures/t1_tap.png')
plt.close()


# --- T2 from spinski odmev ---

data_odmev = np.array(pd.read_csv('../meritve/ion_water_t2.csv',
                                  delimiter=','))

cas_odmev = data_odmev[:-3, 0]
napetost_odmev = np.log(data_odmev[:-3, 1])

fitpar_odmev, fitcov_odmev = curve_fit(linearna, cas_odmev,
                                       napetost_odmev)

t2_nostar = - 1 / unp.uarray(fitpar_odmev[0],
                           np.sqrt(np.diag(fitcov_odmev))[0])
print("T2 ion water: ", t2_nostar)

text2 = 'fit ' + 'k = {:.3f}'.format(fitpar_odmev[0])\
    + ' n = {:.3f}'.format(fitpar_odmev[1])

plt.scatter(cas_odmev, napetost_odmev, color=c1, label='meritev',
            marker='.')
plt.plot(cas_odmev, linearna(cas_odmev, *fitpar_odmev),
         color=c2, label=text2)

plt.xlabel(r'Čas med sunkoma $\frac{\pi}{2}$ in $\pi$')
plt.ylabel(r'$\ln M + \text{konst}$')

plt.legend()
plt.title('Amplituda spinskega odmeva, voda s paramagnetnimi ioni')
plt.savefig('../porocilo/figures/spinski_odmev_t2.png')
plt.close()
