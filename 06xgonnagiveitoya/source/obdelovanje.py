#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cmasher as cms
from uncertainties import unumpy as unp

# ionizacijska celica, meritev nasičenosti

# data for 25kV

data_25kV = pd.read_csv(r'../meritve/ion_cell_25kV.csv',delimiter=';')
data_25kV = np.array(pd.DataFrame(data_25kV, columns=["U_s", "U_E"]))

# data for 30kV

data_30kV = pd.read_csv(r'../meritve/ion_cell_30kV.csv', delimiter=';')
data_30kV = np.array(pd.DataFrame(data_30kV, columns=["U_s", "U_E"]))

# data for 35kV

data_35kV = pd.read_csv(r'../meritve/ion_cell_35kV.csv', delimiter=';')
data_35kV = np.array(pd.DataFrame(data_35kV, columns=["U_s", "U_E"]))

# upor, da lahko izračunamo tok

resistance = 1.e9

# gostota zraka (vir: https://www.calctool.org/atmospheric-thermodynamics/air-density)
rho = 1.18638 #kg/m^3
# volumen celice
volumen = 125.4e-6

# podatke zapišemo v spremenljivke for easier acces, although probably more
# reasonable bi bilo ponovno narediti class iz tega
# 2 stolpec delimo z uporom, da dobimo tok

U_25 = data_25kV[:, 0]
I_25 = data_25kV[:, 1] / resistance
I_25_err = unp.uarray(I_25, len(I_25) * [0.01e-9])

U_30 = data_30kV[:, 0]
I_30 = data_30kV[:, 1] / resistance
I_30_err = unp.uarray(I_30, len(I_30) * [0.01e-9])

U_35 = data_35kV[:, 0]
I_35 = data_35kV[:, 1] / resistance
I_35_err = unp.uarray(I_35, len(I_35) * [0.01e-9])

# nasičenost gledamo in povprečimo na intervalu [100, 300]

I_25_nas = unp.uarray(np.average(I_25[U_25 > 100]), np.std(I_25[U_25 > 100]))
I_30_nas = unp.uarray(np.average(I_30[U_30 > 100]), np.std(I_30[U_30 > 100]))
I_35_nas = unp.uarray(np.average(I_35[U_35 > 100]), np.std(I_35[U_35 > 100]))

print(I_25_nas, '\n', I_30_nas, '\n', I_35_nas, '\n')

# hitrost ekspozicije

x_pikica_25 = I_25_nas / (rho * volumen)
x_pikica_30 = I_30_nas / (rho * volumen)
x_pikica_35 = I_35_nas / (rho * volumen)

print(x_pikica_25, '\n', x_pikica_30, '\n', x_pikica_35, '\n')


# grafi
c1, c2, c3 = cms.take_cmap_colors("cmr.freeze", 3, cmap_range=(0.3, 0.8),
                                  return_fmt='hex')

plt.plot(U_25, unp.nominal_values(I_25_err), alpha=0.5, c=c1)
plt.errorbar(U_25, unp.nominal_values(I_25_err), yerr=unp.std_devs(I_25_err),
             markersize=2, color=c1, ls='None', marker='^', capsize=2,
             label=r'$25 \mathrm{kV}$', alpha=1)
plt.axhline(y=unp.nominal_values(I_25_nas), color='#adadad', ls='--', alpha=0.5)

plt.plot(U_30, unp.nominal_values(I_30_err), alpha=0.5, c=c2)
plt.errorbar(U_30, unp.nominal_values(I_30_err), yerr=unp.std_devs(I_30_err),
             markersize=2, color=c2, ls='None', marker='^', capsize=2,
             label=r'$30 \mathrm{kV}$', alpha=1)
plt.axhline(y=unp.nominal_values(I_30_nas), color='#adadad', ls='--', alpha=0.5)

plt.plot(U_35, unp.nominal_values(I_35_err), alpha=0.5, c=c3)
plt.errorbar(U_35, unp.nominal_values(I_35_err), yerr=unp.std_devs(I_35_err),
             markersize=2, color=c3, ls='None', marker='^', capsize=2,
             label=r'$35 \mathrm{kV}$', alpha=1)
plt.axhline(y=unp.nominal_values(I_35_nas), color='#adadad', ls='--', alpha=0.5)

plt.title('Merjenje toka nasičenja v ionizacijski celici')
plt.xlabel(r'$U_s [\mathrm{V}]$')
plt.ylabel(r'$I_e [\mathrm{A}]$')

plt.legend()
plt.savefig('../porocilo/figures/tok_nasicenja.png')
plt.close()

# --- ionizacija ---

# class za lažjo obravnavo

class Polarizacija:
    def __init__(self, I_x, I_z):
        self.I_x = np.array(pd.DataFrame(I_x, columns=['R/1/s', 'I_x']))
        self.I_z = np.array(pd.DataFrame(I_z, columns=['R/1/s', 'I_z']))

    def average(self):
        x_avg = unp.uarray(np.average(self.I_x[:, 1]), np.std(self.I_x[:, 1]))
        z_avg = unp.uarray(np.average(self.I_z[:, 1]), np.std(self.I_z[:, 1]))
        return x_avg, z_avg

    def polarisation(self):
        eta = (self.average()[1] - self.average()[0]) / (self.average()[0] \
                                                         + self.average()[1])
        return eta

# instance razreda

sipanje_1x = Polarizacija(pd.read_csv('../meritve/1xsip_35kV_kot0.csv',
                                   delimiter=';'),
                       pd.read_csv('../meritve/1xsip_35kV_kot90.csv',
                                   delimiter=';'))
sipanje_2x = Polarizacija(pd.read_csv('../meritve/2xsip_35kV_kot0_kot0.csv',
                                      delimiter=';'),
                          pd.read_csv('../meritve/2xsip_35kV_kot0_kot90.csv',
                                      delimiter=';'))

print(sipanje_1x.average(), '\n', sipanje_1x.polarisation())
print(sipanje_2x.average(), '\n', sipanje_2x.polarisation())
