#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cmasher as cmr
from uncertainties import unumpy as unp
from uncertainties import ufloat

# izmerjeni podatki
a = ufloat(41, 0.5) # razdalja leca - kiveta
b = ufloat(110, 0.5) # razdalja kiveta - zaslon
d = ufloat(1.8, 0.1) # debelina kivete


# --- casovna neodvisnost ploscine S ---
# za ploscino sem uporabil web plot digitizer (https://apps.automeris.io/wpd4/)

ploscina = ((a + b) / a) * d * 0.029 # razlika n_a - n_v = 0.029, podano v navodilih
print('ploscina S tocno: ', ploscina)

# za case t=0, 33.5, 70

kvadratniCm = ufloat(12996, 100) # kvadratnih pixelov na grafu
povrsina = unp.uarray([1362893, 1354984, 1374015], [1000, 5000, 10000])

povrsina3kotnika = 1362893 - 242335
# povrsina trikotnika pod grafom je 86 cm^2, kar pomeni, da to odštejem rezultatom
# in dobim pravilne rezultate.

povrsina -= povrsina3kotnika

print('ploscina S glede na y_max: ', (povrsina/ kvadratniCm))
