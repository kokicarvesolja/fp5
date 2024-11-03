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

# funkciiji za fittanje
#
def model1(omega, psi0, tau):
    return psi0/(1 + (omega * tau)**2)

def model2(omega, psi0, tau):
    return - (psi0 * omega * tau) / (1 + (omega * tau)**2)

# branje podakov - je v redu

data2 = pd.read_csv(r'./meritve/02V.csv')

nu = np.array(data2['nu']) * (2 * np.pi)
x = unp.uarray(data2['X'], (len(data['X']) - 1) * 0.01e-3)
y = unp.uarray(data2['Y'], (len(data['Y']) - 1) * 0.01e-3)

# fittanje podatkov

# poskusil 10, 14, 20, 25
meje1 = 10
meje2 = 30

fitpar1, fitcov1 = curve_fit(model1, nu[meje1:], unp.nominal_values(x)[meje1:])
fitpar2, fitcov2 = curve_fit(model2, nu[meje2:], unp.nominal_values(y)[meje2:]
                             )#, p0=[1, 1], bounds=([0,0], [2, 2]))

print(fitpar2[0], fitpar2[1])

fit1 = model1(nu, *fitpar1)
fit2 = model2(nu, *fitpar2)

fig, ax = plt.subplots()

# plot for real part
plt.errorbar(nu, unp.nominal_values(x), yerr=unp.std_devs(x), markersize=2, ls='None',
             marker='o', label=r'$\psi_r$')
plt.plot(nu, fit1, label='fit real')

# plot for imaginary part
plt.errorbar(nu, unp.nominal_values(y), yerr=unp.std_devs(y), markersize=2, ls='None',
             marker='o', label=r'$\psi_i$')
plt.plot(nu, fit2, label='fit imaginary')

plt.xlabel(r'$\omega [\mathrm{s}^{-1}]$')
plt.ylabel(r'$\psi [\mathrm{V}]$')
plt.legend()
plt.savefig('test.png')
