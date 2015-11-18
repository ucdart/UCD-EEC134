# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 14:40:07 2015

@author: Xiaoguang
"""
import numpy as np

sif1 = np.array([[1.0,2.0,3.0],[4.0,5.0,6.0]])
sif2 = sif1
#subtract the average
M=int(len(sif1))
N=int(len(sif1[0]))

s_T=[[sif1[j][i] for j in range(M)] for i in range(int(N))]#this line is time consuming!
print(s_T)

for k in range(int(N)):
    ave=sum(s_T[k])/M
    print(ave)
    for d in range(M):
        sif1[d][k]=sif1[d][k]-ave

print(sif1)