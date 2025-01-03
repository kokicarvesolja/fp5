#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cmasher as cmr
from uncertainties import unumpy as unp
from uncertainties import ufloat
import pandas as pd

# izmerjeni podatki
a = ufloat(41, 0.5) # razdalja leca - kiveta
b = ufloat(110, 0.5) # razdalja kiveta - zaslon
d = ufloat(1.8, 0.1) # debelina kivete

# colours

c1, c2, c3 = cmr.take_cmap_colors("cmr.gem", 3, cmap_range=(0.2, 1),
                                  return_fmt="hex")
# --- casovna neodvisnost ploscine S ---
# za ploscino sem uporabil web plot digitizer (https://apps.automeris.io/wpd4/)
# File > Load Image. Calibrate by choosing two (x, y) points, than under section
# measurements choose Area and add polygons. Area is given in pixels, so measure
# how much is 1cm^2 in pixels.

k = (a + b) / a

ploscina = k * d * 0.029 # razlika n_a - n_v = 0.029, podano v navodilih
print('ploscina S tocno: ', ploscina)

# za case t=0, 33.5, 70

kvadratniCm = ufloat(12996, 100) # kvadratnih pixelov na grafu
povrsina = unp.uarray([1362893, 1354984, 1374015], [1000, 5000, 10000])

povrsina3kotnika = 1362893 - 242335
# povrsina trikotnika pod grafom je 86 cm^2, kar pomeni, da to odštejem rezultatom
# in dobim pravilne rezultate.

povrsina -= povrsina3kotnika

print('ploscina S glede na y_max: ', (povrsina/ kvadratniCm))

# --- dolocanje difuzijske konstante ---

# risemo graf 1 / (4 * np.pi * k ** 2) * (ploscina / visina) ** 2 v odvisnosti od
# casa

data =np.array(pd.read_csv('../meritve/data.csv', delimiter=','))

time = data[:, 0] / 60
meritve = unp.uarray(data[:, 1], 13 * [0.5]) * 1e-4

meritve = 1 / (4 * np.pi * k ** 2) * (ploscina / meritve) ** 2
