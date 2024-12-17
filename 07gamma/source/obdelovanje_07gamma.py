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
    return energy * 2 * (energy/0.51) / ( 1 + 2 * energy / 0.51 )

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
xcal_Na22_p1 = x_cal[start_peak1:end_peak1]

fitpar_na22_p1, fitcov_na22_p1 = curve_fit(gauss, xcal_Na22_p1,
                                           r_na22[start_peak1:end_peak1], p0=[1,1,1])

sigma_Na1 = unp.uarray(fitpar_na22_p1[2], np.sqrt(np.diag(fitcov_na22_p1))[2])
# širina vrhov je sigma
print('Širina prvega vrha za natrij: ', sigma_Na1)

# calculating energijsko ločljivost according to

E0_Na1 = unp.uarray(fitpar_na22_p1[1], np.sqrt(np.diag(fitcov_na22_p1))[1])

# 2.355 * FWHM je enako sigma Gaussove funkcije
print("R natrija: ", 2.355 * sigma_Na1/E0_Na1)

# računanje preko np.sum(r_na22) ali pa preko np.sqrt(np.sum(r_na22)) ne dela

plt.plot(xcal_Na22_p1, gauss(xcal_Na22_p1, *fitpar_na22_p1), color=e2)

# second peak at 3625

start_peak2 = drugi_max - 250
end_peak2 = drugi_max + 200
xcal_Na22_p2 = x_cal[start_peak2:end_peak2]

fitpar_na22_p2, fitcov_na22_p2 = curve_fit(gauss, xcal_Na22_p2,
                                           r_na22[start_peak2:end_peak2])

sigma_Na2 = unp.uarray(fitpar_na22_p2[2], np.sqrt(np.diag(fitcov_na22_p2))[2])
print('Širina drugega vrhu za natrij: ', sigma_Na2)

# Energijska ločljivost drugega vrha natrija
E0_Na2 = unp.uarray(fitpar_na22_p2[1], np.sqrt(np.diag(fitcov_na22_p2))[1])

print("R drugega vrha natrija: ", 2.355 * sigma_Na2 / E0_Na2)

plt.plot(xcal_Na22_p2, gauss(xcal_Na22_p2, *fitpar_na22_p2), color=e3)

# backscatter and Compton peak, v enačbo vstaviš energijo prvega (ali edinega) vrha

backscatterNa22 = backscatter(0.511)
comptonPeakNa22 = comptonpeak(0.511)

print("Backscatter peak natrija: ", backscatterNa22)
print("Compton peak natrija: ", comptonPeakNa22)

plt.vlines(backscatterNa22, 0, 2.0, color=d3, ls='dotted',
           label="predvideno povratno sipanje")
plt.vlines(comptonPeakNa22, 0, 2.0, color=e1, ls='dotted',
           label='predviden Comptonski vrh')

# plot of bars and energy

plt.bar(x_cal, r_na22, width=0.001, color=d1)
plt.vlines(0.51, 0, 2.0, color=d2, ls = '--', zorder=1,
           label=r'$E_1 = 0.51 \mathrm{MeV}$')
plt.vlines(1.277, 0, 2.0, color=d2, ls = '--', zorder=1,
           label=r'$E_2 = 1.27 \mathrm{MeV}$')
plt.title(r'Spekter $^{22} \mathrm{Na}$ brez ozadja')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.legend()
plt.savefig('../porocilo/figures/na22_no_bg.png')
plt.close()

print('Done plot of natrij without background')

# --- cezij brez šuma ---

dataCs = np.loadtxt('../meritve/Cs137_1.txt')
timeCs = 59.92

# aktivnost cezija

r_cs137 = dataCs / timeCs - r_bg

# getting the index of Cs

argmaxCs = np.argmax(r_cs137[150:]) + 150
print("Vrh cezija: ", x_cal[argmaxCs])

startPeakCs = argmaxCs - 200
endPeakCs = argmaxCs + 200

# adjusting x axis
xCalCs137 = x_cal[startPeakCs:endPeakCs]

fitparCs137, fitcovCs137 = curve_fit(gauss, xCalCs137,
                                     r_cs137[startPeakCs:endPeakCs])

sigmaCs =  unp.uarray(fitparCs137[2], np.sqrt(np.diag(fitcovCs137))[2])
E0Cs = unp.uarray(fitparCs137[1], np.sqrt(np.diag(fitcovCs137))[2])

# širina vrha

print("Širina prvega vrha cezija: ", sigmaCs)
print("R cezija: ", 2.355 * sigmaCs / E0Cs)

# backscatter and Compton peak

backscatterCs = backscatter(E0Cs)
comptonPeakCs = comptonpeak(E0Cs)

print("Backscatter peak Cs: ", backscatterCs)
print("Compton peak Cs: ", comptonPeakCs)

plt.vlines(unp.nominal_values(backscatterCs), 0, 3.5, color=d3, ls='dotted',
           label="predvideno povratno sipanje")
plt.vlines(unp.nominal_values(comptonPeakCs), 0, 3.5, color=e1, ls='dotted',
           label='predviden Comptonski vrh')

# plot of Gauss function

plt.plot(xCalCs137, gauss(xCalCs137, *fitparCs137), color=e3)

# bar plot of cezij
plt.bar(x_cal, r_cs137, width=0.001, color=d1)

# the maximum of cezij
plt.vlines(x_cal[argmaxCs], 0, 3.5, color=d2, ls = '--', zorder=1,
           label=r'$E_1 = (0.66 \pm 0.04) \mathrm{MeV}$')

# miscs for matplotlib
plt.legend()
plt.title(r'Spekter $^{137} \mathrm{Cs}$ brez ozadja')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/Cs137_no_bg.png')
plt.close()

print("Finished plot of Cs")

# --- kobalt brez šuma ---

print("Plot of Co")
dataCo = np.loadtxt('../meritve/Co60.txt')
timeCo = 54.8

# aktivnost kobalta

r_Co60 = dataCo / timeCo - r_bg

# getting first index of Co

argmaxCo1 = np.argmax(r_Co60)
print("Vrh 1 od kobalta: ", x_cal[argmaxCo1])

# getting second index of Co

argmaxCo2 = np.argmax(r_Co60[(argmaxCo1 + 100):]) + (argmaxCo1 + 100)
print("Vrh 2 od Co: ", x_cal[argmaxCo2])

# fitting for the first peak of Co

startPeakCo1 = argmaxCo1 - 300
endPeakCo1 = argmaxCo1 + 300

# adjusting x axis

xCalCo1 = x_cal[startPeakCo1:endPeakCo1]

fitparCo1, fitcovCo1 = curve_fit(gauss, xCalCo1,
                                 r_Co60[startPeakCo1:endPeakCo1])

# energijska ločljivost prvega vrha
sigmaCo1 =  unp.uarray(fitparCo1[2], np.sqrt(np.diag(fitcovCo1))[2])
E0Co1 = unp.uarray(fitparCo1[1], np.sqrt(np.diag(fitcovCo1))[2])

# širina prvega vrha kobalta

print("Širina prvega vrha kobalt: ", sigmaCo1)
print('R prvega vrha Co: ', 2.355 * sigmaCo1 / E0Co1)

plt.plot(xCalCo1, gauss(xCalCo1, *fitparCo1), color=e2)

# backscatter and compton peak of Co
backscatterCo = backscatter(E0Co1)
comptonPeakCo = comptonpeak(E0Co1)

print("Backscatter peak kobalta: ", backscatterCo)
print("Compton peak kobalta: ", comptonPeakCo)


plt.vlines(unp.nominal_values(backscatterCo), 0, 1.5, color=d3, ls='dotted',
           label="predvideno povratno sipanje")
plt.vlines(unp.nominal_values(comptonPeakCo), 0, 1.5, color=e1, ls='dotted',
           label='predviden Comptonski vrh')

# fitting for the second peak of Co

startPeakCo2 = argmaxCo2 - 200
endPeakCo2 = argmaxCo2 + 200

xCalCo2 = x_cal[startPeakCo2:endPeakCo2]

fitparCo2, fitcovCo2 = curve_fit(gauss, xCalCo2,
                                 r_Co60[startPeakCo2:endPeakCo2])

# energijska ločljivost drugega vrha kobalta
sigmaCo2 =  unp.uarray(np.abs(fitparCo2[2]), np.sqrt(np.diag(fitcovCo2))[2])
E0Co2 = unp.uarray(fitparCo2[1], np.sqrt(np.diag(fitcovCo2))[2])

# širina prvega vrha kobalta

print("Širina drugega vrha kobalta: ", sigmaCo2)
print("R drugega vrha Co: ", 2.355 * sigmaCo2 / E0Co2)

plt.plot(xCalCo2, gauss(xCalCo2, *fitparCo2), color=e3)

plt.bar(x_cal, r_Co60, width=0.001, color=d1)

# first peak
plt.vlines(x_cal[argmaxCo1], 0, 1.5, color=d2, ls='--', zorder=1,
           label=r'$E_1 = (1.16 \pm 0.1) \mathrm{eV}$')

# second peak

plt.vlines(x_cal[argmaxCo2], 0, 1.5, color=d2, ls='--', zorder=1,
           label=r'$E_2 = (1.33 \pm 0.1) \mathrm{eV}$')

# miscs for matplotlib
plt.legend()
plt.title(r'Spekter $^{60} \mathrm{Co}$ brez ozadja')
plt.xlabel(r'$E [\mathrm{MeV}]$')
plt.ylabel(r'$R [\mathrm{s} ^{-1}]$')
plt.savefig('../porocilo/figures/Co60_no_bg.png')
plt.close()

# --- izkoristek ---

aktivnost = unp.uarray(np.sum(r_cs137), 2)
A0 = 9250 # podatki iz leta 2013
tau = 30.07 # in years
trenutno = 2024 - 2013

izracunanaAktivnost = A0 * np.exp( - trenutno / tau)
print(izracunanaAktivnost)

effective = aktivnost / izracunanaAktivnost
print('\eta = ', effective)
