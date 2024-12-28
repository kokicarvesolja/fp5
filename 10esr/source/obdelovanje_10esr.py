#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
from uncertainties import unumpy as unp

# function I need

def linear(x, k, n):
    return k * x + n

# colors

c1, c2, c3 = cmr.take_cmap_colors('cmr.lavender', 3, cmap_range=(0.3, 1.0),
                                  return_fmt='hex')

# diagonala tuljave
# krajsi polmer
r_1 = unp.uarray([4.5], [0.1]) # cm
# daljsi polmer
r_2 = unp.uarray([8.7], [0.1]) # cm
# dolzina tuljave
l = unp.uarray([13.2], [0.1]) # cm
# vrednost diagonale
d = unp.sqrt(l**2 + (r_1 + r_2)**2)

print("Vrednost diagonale: ", d)

# --- konstante ---

mi_0 = 4 * np.pi * 1e-7 # Vs/Am
N = 1557

# B0 = N mi_0 I / d, kjer je N = 1557
C = N * mi_0 / d

# --- odvod absorpcijskega vrha ---

# getting data
# 80MHz

data_80MHz = pd.read_csv('../meritve/80MHz.csv', delimiter=',')
# dolzina seznama
len80 = len(data[:, 0])
tok_80MHz = unp.uarray(data_80MHz[:, 0], len80 * [1])
volt_80MHz = unp.uarray(data_80MHz[:, 1], data_80MHz[:, 1] * 0.05)

# extracting maximum and minimum for \Delta B
