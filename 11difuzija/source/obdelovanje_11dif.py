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
