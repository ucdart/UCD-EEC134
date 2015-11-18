# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 00:06:14 2015

@author: Xiaoguang
"""

import numpy as np

ar = np.array([[1.0, 2.0, 3.0],[4.0, 5.0, 6.0]])

M, N = ar.shape

for i in range(N):
 ar[:,i] = ar[:,i] - np.mean(ar[:,i])
 
print(ar)

print(ar[0]+ar[1])

print(ar[0]-1)