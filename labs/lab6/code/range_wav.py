# -*- coding: utf-8 -*-
#range radar, reading files from a WAV file
# Originially modified by Meng Wei, a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China, from Greg Charvat's matlab code
# Nov. 17th, 2015, modified by Xiaoguang "Leo" Liu, lxgliu@ucdavis.edu

import wave
import os
from struct import unpack
import numpy as np
from numpy.fft import ifft
import matplotlib.pyplot as plt 
from math import log

#constants
c= 3E8 #(m/s) speed of light
Tp = 20E-3  #(s) pulse duration T/2, single frequency sweep period. 
fstart = 2260E6 #(Hz) LFM start frequency
fstop = 2590E6 #(Hz) LFM stop frequency
BW = fstop-fstart #(Hz) transmti bandwidth

# for debugging purposes
# log file
#logfile = 'log_new.txt'
#logfh = open(logfile,'w')
#logfh.write('start \n')

#read the raw data .wave file here
#get path to the .wav file
#filename = os.getcwd() + '\\running_outside_20ms.wav'
filename = os.getcwd() + '\\falcon9_9_3.wav'     # The initial 1/6 of the above wav file. To save time in developing the code
#open .wav file
wavefile = wave.open(filename, "rb")

# number of channels
nchannels = wavefile.getnchannels()

# number of bits per sample
sample_width = wavefile.getsampwidth()
print(sample_width)

# sampling rate
Fs = wavefile.getframerate()
print(Fs)

# number of samples per pulse
N = int(Tp*Fs)  ## of samples per pulse

# number of frames (total samples)
numframes = wavefile.getnframes()

#number of rows in the raw data
rows = int(numframes/N)

# for debugging purposes
#count = 0

# the alignment program needs to be improved. 
# the following line is a hack, not very elegant
# we are only using the up-ramp data so the divide by 2. Can be improved in the future.
rows = int(rows/2-120) 

# trig stores the sampled SYNC signal in the .wav file
trig = np.zeros([rows,N])
# s stores the sampled radar return signal in the .wav file
s = np.zeros([rows,N])
# v stores ifft(s)
v = np.zeros([rows,N])

#locate the rising edge 
#triggerng threshold
th = 0

for i in range(rows):
    data = wavefile.readframes(1)[0:2]
    if len(data) ==2:
        trig_cur = unpack('h', data)[0] > th
        trig_prev = trig_cur

# detect rising edge in the SYNC signal
    while trig_cur == trig_prev:
        trig_prev = trig_cur
        trig_cur = unpack('h', wavefile.readframes(1)[0:2])[0] > th
# for debugging purposes
#        count = count +1

# for debugging purposes
#    logfh.write(str(count)+'\n')
    
    data = wavefile.readframes(2*N) # N is determined by Tp. Note that the real Tp in this datafile is more like 22ms. Here Tp=20ms is used. It is OK because we will discard the down-ramp data

# for debugging purposes
#    count = count + 2*N
#    logfh.write(str(count)+'\n')
    
    for j in range(0,N):
        # get the left (SYNC) channel
        left = data[4*j:4*j+2]
        # get the right (Data) channel
        right = data[4*j+2:4*j+4]
        #.wav file store the sound level information in signed 16-bit integers stored in little-endian format
        #The "struct" module provides functions to convert such information to python native formats, in this case, integers.
	if len(left) == 2:
	    v = unpack('h', left)[0]
        if len(right) == 2: 
	    u = unpack('h', right)[0]
        #normalize the value to 1 and store them in a two dimensional array "s"
        trig[i][j] = v/32768.0
        s[i][j] = u/32768.0

# for debugging purposes
#logfh.close()

#pulse-to-pulse averaging to eliminate system performance drift overtime
for i in range(N):
    s[:,i] = s[:,i] - np.mean(s[:,i])

#apply a Hamming window to reduce fft sidelobes
#for i in range(rows):
#    s[i]=np.multiply(s[i],np.hamming(N))

#####################################
# Range-Time-Intensity (RTI) plot
# inverse FFT. By default the ifft operates on the row
v = ifft(s)

#get magnitude
v = 20*np.log10(np.absolute(v)+1e-12)

#only the first half in each row contains unique information
v = v[0:rows,0:int(N/2)]

#normalized with respect to its maximum value so that maximum is 0dB
m=np.max(v)
grid=[[x-m for x in y] for y in v]

# maximum range
max_range =c*Fs*Tp/4/BW
# maximum time
max_time = Tp*rows*2

plt.figure(0)
plt.imshow(grid, extent=[0,max_range,0,max_time],aspect='auto')
plt.colorbar()
plt.clim(0,-100)
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI without clutter rejection',{'fontsize':20})
plt.tight_layout() 
plt.show()

##########################
#two pulse cancelor RTI plot
s2pulse = s

for i in range(rows):
    if rows-i-1 == 0:
        s2pulse[0]=s[0]
    else:    
        s2pulse[rows-i-1] = map(float.__sub__, s[rows-i-1], s[rows-i-2])

v = ifft(s2pulse)

# get magnitude
v = 20*np.log10(np.absolute(v)+1e-12)
#only the first half in each row contains unique information
v = v[0:rows,0:int(N/2)]

#normalized with respect to its maximum value so that maximum is 0
m=np.max(v)
grid=[[x-m for x in y] for y in v]

plt.figure(1)
plt.subplot(611)
plt.imshow(grid, extent=[0,max_range,0,max_time],aspect='auto')
plt.colorbar()
plt.clim(0,-100)
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI with 2-pulse clutter rejection',{'fontsize':20})
plt.tight_layout()
plt.show()

plt.subplot(612)
plt.plot(grid[5])

plt.subplot(613)
plt.plot(grid[6])

plt.subplot(614)
plt.plot(grid[20])

plt.subplot(615)
plt.plot(grid[30])

plt.subplot(616)
plt.plot(grid[40])
