#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cmasher as cmr
from uncertainties import unumpy as unp

# calculate \beta x and other values, put them into report and let the freaking
# magic happen.

# defining class for easier handling
class Oscilo:
    def __init__(self, data, zamaknjenost_ch1, zamaknjenost_ch2):
        self.data = np.array(pd.DataFrame(data, columns=['X', 'CH1', 'CH2']))
        self.zamaknjenost_ch1 = zamaknjenost_ch1
        self.zamaknjenost_ch2 = zamaknjenost_ch2
    #extract time, might need to add time scale as an argument
    def time(self):
        return self.data[:, 0] * 5e-2
    def length(self):
        return np.linspace(0, 6.2, num=1200)
    #extract channel 1 and normalize it (sonda)
    def ch1(self):
        return (self.data[:, 1] - np.min(self.data[:, 1])) / (np.max(self.data[:, 1]) - np.min(self.data[:, 1]))
    # extract channel 2
    def ch2(self):
        return self.data[:, 2]
    # extract channel 2 and normalize it (actual data)
    def ch2_norm(self):
        return (self.data[:, 2] - np.min(self.data[:, 2])) / (np.max(self.data[:, 2]) - np.min(self.data[:, 2]))

# colors

c1, c2, c3 = cmr.take_cmap_colors("cmr.bubblegum", 3, cmap_range=(0,1), return_fmt="hex")

# --- umeritev ---

plt.plot([100, 300, 500], [10, 9, 8], c=c2)
plt.scatter(414,8.43, c=c3, label='Meritev')
plt.scatter([100, 300, 500], [10, 9, 8], c=c1)
plt.title('Umeritvena krivulja')
plt.xlabel('Lega vijaka')
plt.ylabel(r'$\nu [\mathrm{GHz}]$')
plt.legend()
plt.savefig('../figures/umeritev.png')
plt.close()

# --- grafi ---
#
# kratkostično

# colors
c4, c5 = cmr.take_cmap_colors("cmr.bubblegum", 2, cmap_range=(0.25, 0.75), return_fmt="hex")

# kratkostična stena on upper figure
#
kratko = Oscilo(pd.read_csv(r'../meritve/kiki_kratki.csv'), 5.88, 0.087)
fig, ax1 = plt.subplots(2, 1)
ax1[0].scatter(kratko.time(), kratko.ch2(), c=c4, marker='.', label='meritve kratkostične stene', zorder=1)
ax1[0].set_xlabel(r'$t[\mathrm{ms}]$')
ax1[0].set_ylabel(r'signal $[\mathrm{V}]$')
ax1[0].set_title('Kratkostična stena')

# creating a twing axes for kratkostična stena

ax2 = ax1[0].twinx()
ax2.scatter(kratko.time(), kratko.ch1(), c=c5, marker='.', label='sonda', zorder=2)
ax2.set_ylabel(r'potenciometer $[0, 1]$')


# bolometer on the lower figure
bolometer = Oscilo(pd.read_csv(r'../meritve/kiki.csv'), 5.88, 0.0)
ax1[1].scatter(bolometer.time(), bolometer.ch2(), c=c4, marker='.', label='meritve bolometra')
ax1[1].set_xlabel(r'$t[\mathrm{ms}]$')
ax1[1].set_ylabel(r'signal $[\mathrm{V}]$')
ax1[1].set_title('Bolometer')

# creating a twin axes for bolometer

ax3 = ax1[1].twinx()
ax3.scatter(bolometer.time(), bolometer.ch1(), c=c5, marker='.', label='sonda', zorder=10)
ax3.set_ylabel(r'potenciometer $[0, 1]$')

fig.tight_layout()
fig.savefig('../figures/kratkoInBolo')
plt.close()

antena = Oscilo(pd.read_csv(r'../meritve/kik_antena.csv'), 5.88, 0.035)


# --- ubranost ---
# shortening of arrays (using signal on interval 2.0 cm to 6.2 cm)
short_length = bolometer.length()[2.0 <= bolometer.length()]
short_bolometer = bolometer.ch2()[2.0 <= bolometer.length()]
short_kratko = kratko.ch2()[2.0 <= bolometer.length()]

# izračun
# minimum bolometra, napaka je \pm na zadnjo decimalko

minimum = unp.uarray(np.min(short_bolometer), 0.001)
maksimum = unp.uarray(np.max(short_bolometer), 0.001)

indeks_minimuma = np.argmin(short_bolometer)
indeks_maksimuma = np.argmax(short_bolometer)

# drawing data

plt.scatter(short_length, short_bolometer, marker='.', c=c4, label='bolometer')
plt.scatter(short_length, short_kratko, marker='.', c=c5,
            label='kratkostična stena')

# drawing horizontal lines where I took the minimum/maximum value

plt.hlines(short_bolometer[indeks_minimuma], 2.0, 6.21, color=c3)
plt.hlines(short_bolometer[indeks_maksimuma], 2.0, 6.21, color=c3)

# drawing vertical lines for difference between two minimums of bolometer and
# kratkostična stena

# everything else for beautiful graphs
plt.xlabel(r'Razdalja $[\mathrm{cm}]$')
plt.ylabel(r'Signal $[\mathrm{V}]$')
plt.legend()
plt.title('Krivulja ubranosti in uporabljene vrednosti za ubranost $s$')
plt.savefig('../figures/krivulja_ubranosti.png')
plt.close()

# določanje x_min ', kar je razlika med minimumom bolometra in minimumom
# kratkostične stene

# minimum bolometra je določen od prej
#
# minimum kratkostične stene

indeks_minimuma_kratko = np.argmin(short_kratko)


# drawing that on a graph
#
fig_2, ax_2 = plt.subplots()

# drawing data

ax_2.scatter(short_length, short_bolometer, marker='.', c=c4, label='bolometer')
ax_2.scatter(short_length, short_kratko, marker='.', c=c5,
            label='kratkostična stena')

# drawing vertical lines

ax_2.vlines(short_length[indeks_minimuma], -0.21,0.001, color=c3)
ax_2.vlines(short_length[indeks_minimuma_kratko], -0.21,0.001, color=c3)

# annotation arrows

# annotation, look for customizing annotation arrows section
# https://matplotlib.org/stable/users/explain/text/annotations.html#annotations
an1 = ax_2.annotate('',
             xy=(short_length[indeks_minimuma], 0.0), xycoords='data',
             xytext=(short_length[indeks_minimuma_kratko], 0.0),
             textcoords='data', arrowprops=dict(arrowstyle="<->",
             connectionstyle="arc3"))

# text na polovici
# I am referring to object, to create an arrow
# docs: https://matplotlib.org/stable/users/explain/text/annotations.html#annotations
# annotating an artist for text and
ax_2.annotate(r"$x_{min}'$", xy=(.5, -3.5),
              xycoords=an1, fontsize=10.0, textcoords=an1, ha='center',
              va='bottom')

# drawing \lambda '

se_bolj_omejenen_interval_dolzine = bolometer.length()[4.5 <= bolometer.length()]
se_bolj_omejenen_interval_kratko = kratko.ch2()[4.5 <= bolometer.length()]

indeks_drugega_minimuma = np.argmin(se_bolj_omejenen_interval_kratko)
ax_2.vlines(se_bolj_omejenen_interval_dolzine[indeks_drugega_minimuma], -0.21,0.001,
            color=c3)

# puscica in tekst za lambdo

an2 = ax_2.annotate('', xy=(short_length[indeks_minimuma_kratko], 0.0),
                    xycoords='data',
                    xytext=(se_bolj_omejenen_interval_dolzine[indeks_drugega_minimuma], 0.0),
                    textcoords='data', arrowprops=dict(arrowstyle="<->",
                                                       connectionstyle='arc3'))
# annotating this monster

ax_2.annotate(r"$\frac{1}{2}\lambda_{min}'$", xy=(.5,.5), xycoords=an2,
              fontsize=10.0, textcoords=an2, ha='center', va='bottom')

# everything else for beautiful graphs
plt.xlabel(r'Razdalja $[\mathrm{cm}]$')
plt.ylabel(r'Signal $[\mathrm{V}]$')
plt.legend()
plt.title('Krivulja ubranosti in izmerjene vrednosti')
plt.savefig('../figures/krivulja_ubranosti_x_min.png')
plt.close()

# --- kalkulacije ---

# ubranost

s = unp.sqrt(maksimum / minimum)
print('Ubranost s:', s)

# razlika vrednosti za x_min', v unumpy.uarray
# I should have used uncertainties.ufloat, but I am too lazy

x_min_crt = unp.uarray(short_length[indeks_minimuma_kratko] -\
                       short_length[indeks_minimuma], 0.01)
print(r"Vrednost x_min ': ", x_min_crt)

# \lambda' vrednost, kar je vrednost valovanja pri vstopu v valovod

lambda_min_crt = unp.uarray(se_bolj_omejenen_interval_dolzine[indeks_drugega_minimuma]\
                            - short_length[indeks_minimuma_kratko], 0.01) * 2

print("Lambda': ", lambda_min_crt)

# vrednost zmnožka \beta x_min

beta_x_xmin = 2 * np.pi * (x_min_crt / lambda_min_crt)

print("Produkt beta x_min ': ", beta_x_xmin)

# relativna reaktanca bremena

def reaktanca(ubranost, produkt_beta_x):
    return (((ubranost**2 - 1) * unp.tan(produkt_beta_x)) /\
        (1 + (ubranost ** 2) * (unp.tan(produkt_beta_x) ** 2)))

def rezistenca(ubranost, produkt_beta_x):
    return (1 - reaktanca(ubranost, produkt_beta_x) * unp.tan(produkt_beta_x)) * ubranost

print("Reaktanca: ", reaktanca(s, beta_x_xmin))
print("Rezistenca: ", rezistenca(s, beta_x_xmin))

# za moč potrebujem refleksivnost, ki je
# |r_R| ^2 = ((1 - s)/ (1 + s)) ^2
def refleksijski_koeficient(ubranost):
    return ((1 - ubranost) / (1 + ubranost))**2

print("refleksivnost: ", refleksijski_koeficient(s))

# izračun realne moči

def realna_moc(ubranost, moc):
    return (moc / (1 - refleksijski_koeficient(ubranost)))

data_moc = pd.read_csv(r'../meritve/rodovi.csv', delimiter=';')
data_moc = np.array(pd.DataFrame(data_moc, columns=['N', 'U', 'P']))

izracunana_moc = realna_moc(s, data_moc[:, 2])

# print tabelo za latex, ki bo oblike
# U_0 [V] & P_m [mW] & P[mW]
print(str.join('',[f'{U_0:.2f} & {P_m:.2f} & {P:.2f} & \pm {P_err:.0f} \\\\\n'
                   for U_0, P_m, P, P_err in zip(data_moc[:, 1], data_moc[:, 2] * 1e1,
                                                 unp.nominal_values(izracunana_moc) * 1e1,
                                                 unp.std_devs(izracunana_moc) * 1e3)]
               ))

