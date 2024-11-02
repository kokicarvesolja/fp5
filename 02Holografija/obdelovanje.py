#!/usr/bin/env python3


from uncertainties import unumpy as unp
import numpy as np

a = unp.uarray([94], [1])
x = unp.uarray([255], [5])
lamba = unp.uarray([632.8e-6], [0])

kot = np.arcsin(94 / 255)# * 180 / np.pi
kot_err = np.arcsin(1 / 5)# * 180 / np.pi

d = lamba / (x / a)
print('d: ', d * 1e6, '\n', 'alpha: ', unp.uarray(kot, kot_err))
