# -*- coding: utf-8 -*-
#range radar, reading files from a WAV file
#Written by Meng Wei, a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China


import wave
import os
from struct import unpack
import numpy as np
from numpy.fft import ifft, ifft2
import matplotlib.pyplot as plt 
from math import log

#constants
c= 3E8 #(m/s) speed of light
Tp = 20E-3  #(s) pulse duration T/2, single frequency sweep period
fstart = 2260E6 #(Hz) LFM start frequency
fstop = 2590E6 #(Hz) LFM stop frequency
BW = fstop-fstart #(Hz) transmti bandwidth

# log file
logfile = 'log_new.txt'
logfh = open(logfile,'w')
logfh.write('start \n')

#read the raw data .wave file here
#get path to the .wav file
#filename = os.getcwd() + '\\running_outside_20ms.wav'
filename = os.getcwd() + '\\output.wav'
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

#range resolution
#rr = c/(2*BW)

# number of frames (total samples)
numframes = wavefile.getnframes()

#number of rows
rows = int(numframes/N)

#locate the rising edge 
#triggerng threshold
th = 0

count = 0


#wavefile.rewind()

rows = int(rows/2-20) 
# trig stores the sampled data in the .wav file
trig = np.zeros([rows,N])
# s stores the sampled data in the .wav file
s = np.zeros([rows,N])

for i in range(rows):
    trig_cur = unpack('h', wavefile.readframes(1)[0:2])[0] > th
    trig_prev = trig_cur

    while trig_cur == trig_prev:
        trig_prev = trig_cur
        trig_cur = unpack('h', wavefile.readframes(1)[0:2])[0] > th
        count = count +1

    logfh.write(str(count)+'\n')
    
    data = wavefile.readframes(2*N)

    count = count + 2*N
    logfh.write(str(count)+'\n')
    
    for j in range(0,N):
        # get the left channel
        left = data[4*j:4*j+2]
        # get the right channel
        right = data[4*j+2:4*j+4]
        #.wav file store the sound level information in signed 16-bit integers stored in little-endian format
        #The "struct" module provides functions to convert such information to python native formats, in this case, integers.
        v = unpack('h', left)[0]
        u = unpack('h', right)[0]
        #normalize the value to 1 and store them in a two dimensional array "s"
        trig[i][j] = v/32768.0
        s[i][j] = u/32768.0
        #trig.append((v+2**15-32768)*-1.0/32768.0)
        #s.append((u+2**15-32768)*-1.0/32768.0)

logfh.close()

# #subtract the average
# M=int(len(sif))
# s_T=[[sif[j][i] for j in range(M)] for i in range(int(N))]#this line is time consuming!
#
# for k in range(int(N)):
#     ave=sum(s_T[k])/M
#     for d in range(M):
#         sif[d][k]=sif[d][k]-ave
#
#zpad = int(8*N/2)
#
##subtract the average DC term here
mean=np.mean(s)
s = [[x - mean for x in y] for y in s]
#zpad = int(8*N/2)
#
##apply a Hamming window to reduce fft sidelobes
##for i in range(rows):
##    s[i]=np.multiply(s[i],np.hamming(N))
#
##RTI plot
# inverse FFT
#v=ifft(s)  #now v is a [[]]
#v=ifft(s,zpad,1)  #now v is a [[]]

v = [ifft(s[i]) for i in range(rows)]
#
##get magnitude
v=[[20*log(abs(x)+1e-12,10) for x in y]for y in v]
#
##only the first half in each row contains unique information
S=[x[:int(len(v[0])/2)] for x in v]
m=np.max(S)
#
#normalized with respect to its maximum value so that maximum is 0
grid=[[x-m for x in y] for y in S]
#
# maximum range
max_range =c*Fs*Tp/4/BW
# maximum time
max_time = Tp*len(s)
#
plt.figure(0)
plt.imshow(grid, extent=[0,max_range,0,max_time],aspect='auto')
plt.colorbar()
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI without clutter rejection',{'fontsize':20})
plt.tight_layout() 
plt.show()

s2pulse = s
#2 pulse cancelor RTI plot
for i in range(rows):
    if rows-i-1 == 0:
        s2pulse[0]=s[0]
    else:    
        s2pulse[rows-i-1] = map(float.__sub__, s[rows-i-1], s[rows-i-2])

#p=sif[1:M]
#q=sif[0:M-1]
#sif2=[]
#for i in range(M-1):
#sif2.append(map(float.__sub__, p[i], q[i]))
v = [ifft(s2pulse[i]) for i in range(rows)]

# get magnitude
v=[[20*log(abs(x)+1e-12,10) for x in y]for y in v]

S=[x[:int(len(v[0])/2)] for x in v]
m=np.max(S)

grid=[[x-m for x in y] for y in S]

plt.figure(1)
plt.imshow(grid, extent=[0,max_range,0,max_time],aspect='auto')
plt.colorbar()
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI with 2-pulse cancelor clutter rejection',{'fontsize':20})
plt.tight_layout()
plt.show()
