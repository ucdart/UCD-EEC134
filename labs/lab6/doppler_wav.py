# -*- coding: utf-8 -*-
#Doppler speed calculation and display using data read from a WAV file
# Originally written by Meng Wei,  a summer exchange student (UCD GREAT Program, 2013) from Zhejiang University, China
# Modified by Xiaoguang "Leo" Liu (lxgliu@ucdavis.edu), Aug.2015

import os
import wave
from struct import unpack
import numpy as np
from numpy.fft import fft
from math import log
import matplotlib.pyplot as plt

#constants
c= 3E8 #(m/s) speed of light
fc=2590E6  #transmitting frequency of the radar
Tp = 0.2 #(s) pulse time

#read the raw data .wav file here
#get path to the .wav file
filename = os.getcwd() + '\\highway_doppler.wav'

#.wav file header information
wavefile = wave.open(filename, "rb")

#sampling rate
FS = wavefile.getframerate()

N = int(Tp*FS)  ## of samples per pulse

numframes = wavefile.getnframes()
#numframes = N*4

#number of rows
rows = int(numframes/N)

#s stores the sampled data in the .wav file
s=np.zeros([rows,N])

for i in range(0,rows):
    data = wavefile.readframes(N)
    for j in range(0,N):
        #get the right channel
        right = data[4*j+2:4*j+4]
        #.wav file store the sound level information in signed 16-bit integers stored in little-endian format
        #The "struct" module provides functions to convert such information to python native formats, in this case, integers.
        u = unpack('h', right)[0]            
        #normalize the value to 1 and store them in a two dimensional array "s"        
        s[i][j]=u/32768.0

#subtract the average DC term here
mean=np.mean(s)
s = [[x - mean for x in y]for y in s]
zpad = int(8*N/2)

#apply a Hamming window to reduce fft sidelobes
for i in range(0,rows):
    s[i]=np.multiply(s[i],np.hamming(N))
    
#doppler vs. time plot
v=fft(s)  #now v is a [[]]

#get magnitude
v=[[20*log(abs(x),10) for x in y]for y in v]

#only the first half in each row contains unique information
S=[x[:int(len(v[0])/2)] for x in v]
m=np.max(S)

#normalized with respect to its maximum value so that maximum is 0
grid=[[x-m for x in y] for y in S]

#calculate velocity
delta_f = FS/2
lambdaa=c/fc;
velocity = delta_f*lambdaa/2;
#calculate time
time = Tp*len(v)
plt.figure()
plt.imshow(grid, extent=[0,velocity,0,time],aspect='auto')
plt.xlim(0,30)
plt.colorbar()
plt.xlabel('Velocity (m/sec)',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('doppler',{'fontsize':20})
plt.tight_layout() 
plt.show()  
