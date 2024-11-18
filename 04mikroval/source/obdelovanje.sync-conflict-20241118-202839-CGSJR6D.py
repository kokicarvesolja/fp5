#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cmasher as cmr

# figure out how to organise the z order of twinx graphs

# defining class for easier handling
class Oscilo:
    def __init__(self, data, zamaknjenost_ch1, zamaknjenost_ch2):
        self.data = np.array(pd.DataFrame(data, columns=['X', 'CH1', 'CH2']))
        self.zamaknjenost_ch1 = zamaknjenost_ch1
        self.zamaknjenost_ch2 = zamaknjenost_ch2
    #extract time, might need to add time scale as an argument
    def time(self):
        return self.data[:, 0] * 5e-2
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
#plt.scatter(kratko.time(), kratko.ch1(), c=c4, marker='.',label='sonda')
#plt.scatter(kratko.time(), kratko.ch2_norm(), c=c5, marker='.',label='meritve')
#plt.title('Meritve s kratkostično steno')
#plt.legend()
#plt.savefig('../figures/test.png')
#plt.close()

antena = Oscilo(pd.read_csv(r'../meritve/kik_antena.csv'), 5.88, 0.035)
#plt.plot(antena.time(), antena.ch1(), c=c4, marker='.',label='sonda')
#plt.plot(antena.time(), antena.ch2_norm(), c=c5, marker='.',label='meritve')
#plt.title('Meritve z anteno')
#plt.legend()
#plt.savefig('../figures/test_antena.png')
#plt.close()

#plt.plot(bolometer.time(), bolometer.ch1(), c=c4, marker='.',label='sonda')
#plt.plot(bolometer.time(), bolometer.ch2_norm(), c=c5, marker='.',label='meritve')
#plt.title('Meritve z bolometrom')
#plt.legend()
#plt.savefig('../figures/test_bolometer.png')
#plt.close()

# krivulja ubranosti
#plt.scatter(kratko.time(), kratko.ch2(), c=c4, marker='.', label='kratko')
#plt.scatter(bolometer.time(), bolometer.ch2(), c=c5, marker='.', label='bolometer')
#
#plt.legend()
#plt.savefig('../figures/kratkoInBolo.png')
#plt.close()


# data might be wrong
