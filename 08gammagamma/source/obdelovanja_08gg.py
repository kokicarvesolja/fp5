#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cmasher as cmr
from uncertainties import unumpy as unp
import pandas as pd

'''
Vprašanja, ki mi jih je postavil asistent:
- Kaj je koincidenca? Ker ne moremo biti neskončno natančni je to dogodek, ki ga
zaznamo z dvema scintilatorjema ob približno istem času (nek majhen interval časa)
- Kako smo izmerili TDC ločljivost? Signal enega scintilatorja smo zvezali na oba
kanala smo vezali na RedPitayjo - če bi bila popolnoma natančno bi bilo vse na
povprečnem času, vendar ker ni so Gaussovo razpršene okoli povprečne vrednosti
'''

# all the colors

# colors used
c1, c2, c3 =  cmr.take_cmap_colors('cmr.cosmic', 3, cmap_range=(.5, 1.),
                                   return_fmt='hex')

# functions needed

def linear(x, k, n):
    return k * x + n

# testing casovna locljivost z Gaussom

def gauss(x, C, mi, sigma):
    return C * np.exp(- (x - mi) ** 2 / (2 * sigma ** 2))

# for eliminating zero and negative values

def masking(x, y):
    mask = x > 0
    return x[mask], y[mask]

# --- časovna ločljivost ---

dataCasLoc = np.loadtxt('../meritve/casovna_locljivost_data.txt')

plt.bar(dataCasLoc[:, 0], dataCasLoc[:, 1], width=0.005, color=c1)

fitparCasLoc, fitcovCasLoc = curve_fit(gauss, dataCasLoc[:, 0], dataCasLoc[:, 1])

print("C, mi, sigma: ", fitparCasLoc, np.sqrt(np.diag(fitcovCasLoc)))

gauss_fit = gauss(dataCasLoc[:, 0], *fitparCasLoc)

plt.plot(dataCasLoc[:, 0], gauss_fit, color=c3, label='regresija')
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

casRadRaz = dataRadRaz[:, 0] /1e9
meritveRadRaz = dataRadRaz[:, 1] / casMerjenjaRadRaz

# Graf radioaktivnih razpadov

plt.bar(casRadRaz, meritveRadRaz, width=0.1, color=c1)

plt.xlabel(r'$t [\mathrm{ms}]$')
plt.ylabel(r'$R [\mathrm{s}^{-1}]$')
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

print(unp.uarray(fitparRadRaz[0], napake[0]) * 1e3)

# --- koincidenčni vrh in naključne koincidence ---

# koincidenčni vrh

dataKoinc = np.loadtxt('../meritve/stevilo_koincidenc_data.txt')

timeKoinc = 30.0 #sekund

casKoinc = dataKoinc[:, 0] / 1e6
meritveKoinc = dataKoinc[:, 1] / timeKoinc

plt.bar(casKoinc, meritveKoinc, width=0.5e-5, color=c1)
plt.xlabel(r'$t [\mathrm{ms}]$')
plt.ylabel(r'$R [\mathrm{s}^{-1}]$')
plt.title('Koincidenčni vrh')
plt.savefig('../porocilo/figures/koincidencni_vrh.png')
plt.close()

# nakljucni koincidencni vrh

dataRandKoinc = np.loadtxt('../meritve/nakljucne_koincidence_data.txt')

timeRandKoinc = 30.1 # sekund

casRandKoinc = dataRandKoinc[:, 0] / 1e6
meritveRandKoinc = dataRandKoinc[:, 1] / timeRandKoinc

plt.bar(casRandKoinc, meritveRandKoinc, width=0.5e-5, color=c1)
plt.xlabel(r'$t [\mathrm{ms}]$')
plt.ylabel(r'$R [\mathrm{s}^{-1}]$')
plt.title('Nakljucni koincidenčni vrh')
plt.savefig('../porocilo/figures/nakljucne_koincidence.png')
plt.close()

# --- koincidenčna odvisnost ---


class Koincidenca:
    def __init__(self, data):
        self.data = np.loadtxt(data)

    def cas(self):
        return self.data[:, 0] /1e6

    def meritve(self, time):
        return self.data[:, 1] / time

sez = ['00', '05', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
colors = cmr.take_cmap_colors('cmr.cosmic', len(sez), cmap_range=(.3, 1.),
                              return_fmt='hex')

for num, col in zip(sez, colors):
    # instanca razreda
    kot = Koincidenca(f'../meritve/koincidence_kot{num}_data.txt')
    plt.bar(kot.cas(), kot.meritve(30.1), color=col, width=0.5e-5, label=(fr'$\varphi =$ {num}' + r'$^{\circ}$'))

plt.xlabel(r'$t [\mathrm{ms}]$')
plt.ylabel(r'$R [\mathrm{s}^{-1}]$')
plt.title('Kotna korelacija koincidenčnih vrhov')
plt.legend()
plt.savefig('../porocilo/figures/koincidence_kot.png')
plt.close()
