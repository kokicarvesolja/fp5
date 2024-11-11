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
plt.close()


# --- Second part ---

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
meje1 = 25
meje2 = 30

fitpar1, fitcov1 = curve_fit(model1, nu[meje1:], unp.nominal_values(x)[meje1:])
fitpar2, fitcov2 = curve_fit(model2, nu[meje2:], unp.nominal_values(y)[meje2:]
                             )#, p0=[1, 1], bounds=([0,0], [2, 2]))


fit1 = model1(nu, *fitpar1)
fit2 = model2(nu, *fitpar2)


# plot for real part
plt.errorbar(nu, unp.nominal_values(x), yerr=unp.std_devs(x), markersize=2, ls='None',
             marker='o', label=r'$\psi_r$')
plt.plot(nu, fit1, label='fit real')

# for some reason I had to divide the string into multiple parts
fittext1 = r'Model fit: $\psi_r$' + '\n' + r'$\psi_0$ = {} ± {}'\
    .format(format(fitpar1[0], ".4e"), format(fitcov1[0][0]**0.5, ".4e")) + '\n' + r'$\tau$ = {} ± {}'\
    .format(format(fitpar1[1], ".4e"), format(fitcov1[1][1]**0.5, ".4e"))
plt.text(0.35, 0.35, fittext1, ha="left", va="center", size=10, transform=ax.transAxes,
         bbox=dict(facecolor='tab:orange', alpha=0.5))

# plot for imaginary part
plt.errorbar(nu, unp.nominal_values(y), yerr=unp.std_devs(y), markersize=2, ls='None',
             marker='o', label=r'$\psi_i$')
plt.plot(nu, fit2, label='fit imaginary')

fittext2 = r'Model fit: $\psi_i$' + '\n' + r'$\psi_0$ = {} ± {}'\
   .format(format(fitpar2[0], ".4e"), format(fitcov2[0][0]**0.5, ".4e")) + '\n' + r'$\tau$ = {} ± {}'\
    .format(format(fitpar2[1], ".4e"), format(fitcov2[1][1]**0.5, ".4e"))
plt.text(0.35, 0.20, fittext2, ha="left", va="center", size=10, transform=ax.transAxes,
         bbox=dict(facecolor='r', alpha=0.5))

plt.xlabel(r'$\omega [\mathrm{s}^{-1}]$')
plt.ylabel(r'$\psi [\mathrm{V}]$')
plt.legend()
plt.savefig('fit_modelov.pdf')
plt.close()
print(r'$\tau_1$: ', fitpar1[1] * 1e4,  fitcov1[1][1] ** 0.5 * 1e4)
print(r'$\tau_2$: ', fitpar2[1] * 1e4,  fitcov2[1][1] ** 0.5 * 1e4)


# --- Third part ---

# fittanje


deljeno = y / x

meja3 = 25
meja3_k = len(deljeno) - 15

fitpar3, fitcov3 = curve_fit(linear, nu[meja3:meja3_k], unp.nominal_values(deljeno)[meja3:meja3_k])

fit3 = linear(nu[meja3:meja3_k], *fitpar3)

fittext3 = "Linear fit: $y = kn + n$\n$k$ = {} ± {}\n$n$ = {} ± {}".format(format(fitpar3[0], ".4e"), format(fitcov3[0][0]**0.5, ".4e"),
                                                                           format(fitpar3[1], ".4e"), format(fitcov3[1][1]**0.5, ".4e"))
plt.text(0.35, 0.45, fittext3, ha="left", va="center", size=10, transform=ax.transAxes,
         bbox=dict(facecolor='b', alpha=0.5))

plt.errorbar(nu[meja3:meja3_k], unp.nominal_values(deljeno)[meja3:meja3_k], yerr=unp.std_devs(deljeno)[meja3:meja3_k], markersize=2, ls='None', marker='o', label=r'$\frac{\psi_i}{\psi_r}$')
plt.plot(nu[meja3:meja3_k], fit3, label='fit')

plt.title('Razmerje med signaloma')
plt.xlabel(r'$\omega [\mathrm{s} ^{-1}]$')
plt.ylabel(r'$\frac{\psi_i}{\psi_r}$')
plt.legend()
plt.savefig('deljena.pdf')
print(r'$\tau_3$: ',  fitpar3[0] * 1e4, fitcov3[0][0] ** 0.5 * 1e4)
