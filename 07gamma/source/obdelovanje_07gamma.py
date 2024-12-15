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
'''
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
'''

#--- večkanalne meritve ---

# kalibracija

def linearna(x, k, n):
    return k * x + n

def gauss(x, C, mi, sigma):
    return C * np.exp(- (x - mi) ** 2 / (2 * sigma ** 2))


def backscatter(energy):
    return energy/(1 + 2 * energy/0.51)

def comptonpeak(energy):
    return energy * 2 * (energy/0.51) ( 1 + 2 * energy / 0.51 )

# more colors

d1, d2, d3 = cmr.take_cmap_colors('cmr.cosmic', 3, cmap_range=(.3, .8),
                              return_fmt='hex')
e1, e2, e3 = cmr.take_cmap_colors('cmr.ember', 3, cmap_range=(.3, 1),
                              return_fmt='hex')

# kalibracija z natrijem

calna_cas = 157.8
data_cal = np.loadtxt('../meritve/nacal.txt')

# indeksi znanih maksimumov
maks1, argmax = np.max(data_cal), np.argmax(data_cal)

maks2, argmax2 = np.max(data_cal[1800:]), np.argmax(data_cal[1800:])

# indeksa vrhov 0.51 in 1.277 MeV sta pri indeksih
prvi_max = 1493
drugi_max = 1800 + 1825
fitpar, fitcov = curve_fit(linearna, [prvi_max, drugi_max],\
                           [0.51, 1.277])
# predpostavljam, da je kalibracija linearna, which according to
# Marko's Chest ni. Ampak se mi ne da ponovno delati stvari.
x_cal = linearna(np.arange(0, len(data_cal)), *fitpar)

'''
plt.bar(x_cal, data_cal/calna_cas, width=0.001, color=d1)
plt.vlines(0.51, 0, 2.0, color=d2, ls = '--')
plt.vlines(1.277, 0, 2.0, color=d2, ls = '--')
plt.title(r'Spekter $^{22} \mathrm{Na}$')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/kalibracija.png')
plt.close()
'''
print('done calibrating')

# šum ozadja

data_bg = np.loadtxt('../meritve/bg.txt') # real data doesn't start until line 85
time_bg = 657

'''
plt.bar(x_cal, data_bg/time_bg, width=0.001, color=d1)
plt.title('Šum ozadja')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/ozadje.png')
'''

print('done background noise')

# aktivnost označena z R

r_bg = data_bg / time_bg

# ---  natrij brez šuma ---

data_na22 = np.loadtxt('../meritve/Na22_1.txt')
time_na22 = 54.15

# aktivnost natrija brez ozadja

r_na22 = data_na22 / time_na22 - r_bg

# plotting Gaussian curves
# first peak at 1493

start_peak1 = 1493 - 150
end_peak1 = 1493 + 150

# omejim x_cal za lažji plot
xcal_Na22_p1 = x_cal[start_peak1: end_peak1]

fitpar_na22_p1, fitcov_na22_p2 = curve_fit(gauss, xcal_Na22_p1,
                                           r_na22[start_peak1:end_peak1], p0=[1,1,1])

plt.plot(xcal_Na22_p1, gauss(xcal_Na22_p1, *fitpar_na22_p1), color=e2)

# second peak at 3625

start_peak2 = drugi_max - 250
end_peak2 = drugi_max + 200
xcal_Na22_p2 = x_cal[start_peak2:end_peak2]

fitpar_na22_p2, fitcov_na22_p2 = curve_fit(gauss, xcal_Na22_p2,
                                           r_na22[start_peak2:end_peak2])
plt.plot(xcal_Na22_p2, gauss(xcal_Na22_p2, *fitpar_na22_p2), color=e3)

plt.bar(x_cal, r_na22, width=0.001, color=d1)
plt.vlines(0.51, 0, 2.0, color=d2, ls = '--', zorder=1)
plt.vlines(1.277, 0, 2.0, color=d2, ls = '--', zorder=1)
plt.title(r'Spekter $^{22} \mathrm{Na}$ brez ozadja')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/na22_no_bg.png')
plt.close()

print('Done plot of natrij without background')
