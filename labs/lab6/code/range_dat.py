# -*- coding: utf-8 -*-
# Radar range data processing for EEC134AB. 
# Reading files from a custom .dat file. The file is delimited by ', '. The first column contains the signal. The second column contains the SYNC signal. 
# Originially modified by Meng Wei, a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China, from Greg Charvat's matlab code
# Nov. 17th, 2015, modified by Xiaoguang "Leo" Liu, lxgliu@ucdavis.edu
# Dec. 2, 2018, modified by Xiaoguang "Leo" Liu, lxgliu@ucdavis.edu


import numpy as np
from numpy.fft import ifft
import matplotlib.pyplot as plt 
from math import log

#constants
c= 3E8 # speed of light (m/s)
Tp = 30E-3  # pulse duration T/2 (s). Single frequency sweep period. 
fstart = 2260E6 # LFM start frequency (Hz)
fstop = 2590E6 # LFM stop frequency (Hz)
BW = fstop-fstart # transmit bandwidth (Hz)
#trnc_time = 0 #number of seconds to discard at the begining of the wav file
Fs = 50000   #sampling rate (Hz)
N = int(Tp*Fs)  # number of samples per pulse

window = True  #whether to apply a Hammng window. 

#read recorded data from the .dat file
data = np.loadtxt('example.dat', delimiter=', ')

s = data[:,0]
trig = data[:,1]

#trigger at the rising edge of the SYNC signal
trig[trig < 0.1] = 0;
trig[trig > 0.1] = 1;

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
    
#apply a Hamming window to reduce fft sidelobes if window=True
if window == True:
    for i in range(rows):
        s3[i]=np.multiply(s3[i],np.hamming(N))

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
#plt.imshow(grid, extent=[0,max_range,0,max_time],aspect='auto', cmap =plt.get_cmap('gray'))
plt.imshow(grid, extent=[0,max_range,0,max_time], aspect='auto')
plt.colorbar()
plt.clim(0,-100)
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI with 2-pulse clutter rejection',{'fontsize':20})
plt.tight_layout() 
plt.show()