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

# kalibracija

def linearna(x, k, n):
    return k * x + n

def gauss(x, mi, sigma, C):
    return (C / sigma * np.sqrt(2 * np.pi)) *\
        np.exp(- (1 / 2) * (x - mi) ** 2 / (sigma ** 2))

def gauss_indeks(array, start_indeks, end_indeks):
    indeks = np.arange(len(array))
    fitpar_g, fitcov_g = curve_fit(gauss, indeks[a:b], array[a:b])
    return fitpar_g

def backscatter(energy):
    return energy/(1 + 2 * energy/0.51)

def comptonpeak(energy):
    return energy * 2 * (energy/0.51) ( 1 + 2 * energy / 0.51 )

# more colors

d1, d2, d3 = cmr.take_cmap_colors('cmr.cosmic', 3, cmap_range=(.3, .8),
                              return_fmt='hex')

# kalibracija z natrijem

calna_cas = 157.8
data_cal = np.loadtxt('../meritve/nacal.txt')

# indeksi znanih maksimumov
maks1, argmax = np.max(data_cal), np.argmax(data_cal)
#print('arg max: ', argmax)
#print('maks1: ', maks1)

maks2, argmax2 = np.max(data_cal[1800:]), np.argmax(data_cal[1800:])
#print('arg max: ', argmax2)
#print('maks1: ', maks2)

# indeksa vrhov 0.51 in 1.277 MeV sta pri indeksih
prvi_max = 1493
drugi_max = 1800 + 1825
fitpar, fitcov = curve_fit(linearna, [prvi_max, drugi_max],\
                           [0.51, 1.277])
# predpostavljam, da je kalibracija linearna, which according to
# Marko's Chest ni. Ampak se mi ne da ponovno delati stvari.
x_cal = linearna(np.arange(0, len(data_cal)), *fitpar)

plt.bar(x_cal, data_cal/calna_cas, width=0.001, color=d1)
plt.vlines(0.51, 0, 2.0, color=d2, ls = '--')
plt.vlines(1.277, 0, 2.0, color=d2, ls = '--')
plt.title(r'Spekter $^{22} \mathrm{Na}$')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/kalibracija.png')

print('done calibrating')

# šum ozadja

data_bg = np.loadtxt('../meritve/bg.txt') # real data doesn't start until line 85
time_bg = 657

plt.bar(x_cal, data_bg/time_bg, width=0.001, color=d1)
plt.title('Šum ozadja')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/ozadje.png')

print('done background noise')

# natrij brez šuma



# aktivnost označena z R


r_bg = data_bg / time_bg
