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
BW = fstop-fstart #(Hz) transmit bandwidth
Trunc = 0 #number of seconds to truncate at the begining of the wav. file

# for debugging purposes
# log file
#logfile = 'log_new.txt'
#logfh = open(logfile,'w')
#logfh.write('start \n')

#read the raw data .wave file here
#get path to the .wav file
#filename = os.getcwd() + '\\running_outside_20ms.wav'
filename = os.getcwd() + '\\test58.wav'     # The initial 1/6 of the above wav file. To save time in developing the code
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

# trig stores the sampled SYNC signal in the .wav file
#trig = np.zeros([rows,N])
trig = np.zeros([numframes - Trunc*Fs])
# s stores the sampled radar return signal in the .wav file
#s = np.zeros([rows,N])
s = np.zeros([numframes - Trunc*Fs])
# v stores ifft(s)
#v = np.zeros([rows,N])
v = np.zeros([numframes - Trunc*Fs])

#read data from wav file

data = wavefile.readframes(numframes)

for j in range(Trunc*Fs,numframes):
    # get the left (SYNC) channel
    left = data[4*j:4*j+2]
    # get the right (Data) channel
    right = data[4*j+2:4*j+4]
    #.wav file store the sound level information in signed 16-bit integers stored in little-endian format
    #The "struct" module provides functions to convert such information to python native formats, in this case, integers.
    
    if len(left) == 2:
        l = unpack('h', left)[0]
    if len(right) == 2: 
	  r = unpack('h', right)[0]
        #normalize the value to 1 and store them in a two dimensional array "s"
    trig[j-Trunc*Fs] = l/32768.0
    s[j-Trunc*Fs] = r/32768.0
       
#trigger at the rising edge of the SYNC signal
trig[trig < 0] = 0;
trig[trig > 0] = 1;

#2D array for coherent processing
s2 = np.zeros([int(len(s)/N),N])

rows = 0;
for j in range(10, len(trig)):
    if trig[j] == 1 and np.mean(trig[j-10:j]) == 0:
        if j+N <= len(trig):
            s2[rows,:] = s[j:j+N]
            rows += 1

s2 = s2[0:rows,:]

#pulse-to-pulse averaging to eliminate system performance drift overtime
for i in range(N):
    s2[:,i] = s2[:,i] - np.mean(s2[:,i])

#2pulse cancelation

s3 = s2
for i in range(0, rows-1):
    s3[i,:] = s2[i+1,:] - s2[i,:]
    
rows = rows-1
s3 = s3[0:rows,:]
    
#apply a Hamming window to reduce fft sidelobes
#for i in range(rows):
#    s[i]=np.multiply(s[i],np.hamming(N))

#####################################
# Range-Time-Intensity (RTI) plot
# inverse FFT. By default the ifft operates on the row
v = ifft(s3)

#get magnitude
v = 20*np.log10(np.absolute(v)+1e-12)

#only the first half in each row contains unique information
v = v[:,0:int(N/2)]

#normalized with respect to its maximum value so that maximum is 0dB
m=np.max(v)
grid = v
grid=[[x-m for x in y] for y in v]

# maximum range
max_range =c*Fs*Tp/4/BW
# maximum time
max_time = Tp*rows

plt.figure(0)
plt.imshow(grid, extent=[0,max_range,0,max_time],aspect='auto', cmap =plt.get_cmap('gray'))
plt.colorbar()
plt.clim(0,-100)
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI without clutter rejection',{'fontsize':20})
plt.tight_layout() 
plt.show()

#plt.subplot(612)
#plt.plot(grid[5])

#plt.subplot(613)
#plt.plot(grid[6])

#plt.subplot(614)
#plt.plot(grid[20])
#
#plt.subplot(615)
#plt.plot(grid[30])

#plt.subplot(616)
#plt.plot(grid[40])
