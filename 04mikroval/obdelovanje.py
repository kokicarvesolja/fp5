#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

data = pd.read_csv(r'./meritve/kiki_kratki.csv')
data = np.array(pd.DataFrame(data, columns=['X','CH1','CH2']))

#plt.plot(data[0], data[1])
plt.plot(data[:,0], data[:, 2])
plt.savefig('test')

print(data)
