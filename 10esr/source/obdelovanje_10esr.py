#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import cmasher as cmr
from uncertainties import unumpy as unp

# function I need

def linear(x, k, n):
    return k * x + n

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
