# -*- coding: utf-8 -*-
#Doppler Radar, Read data from a WAV file
#written by Meng Wei,  a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China

import wave
from struct import unpack
from numpy.fft import ifft
from math import log
import matplotlib.pyplot as plt


#read the raw data .wave file here
wavefile = wave.open(r"/boot/Off of Newton Exit 17.wav", "rb")
framerate = wavefile.getframerate()
numframes = wavefile.getnframes()

s=[]
for i in range(numframes):
    val = wavefile.readframes(1)
    right = val[2:4]
    u = unpack('h', right )[0]
    s.append(u*(-1.0)/32768.0)

#constants
c= 3E8 #(m/s) speed of light

#radar parameters
FS=framerate
Tp = 0.250 #(s) pulse time
N = Tp*FS  ## of samples per pulse
fc=2590E6

#creat doppler vs. time plot data set here
sif=[]
for ii in range(1,int(round(len(s)/N))):
             sif.append(s[int((ii-1)*N):int(ii*N)])
          
#subtract the average DC term here
me=sum(s)/len(s)
sif = [[x - me for x in y]for y in sif]
zpad = int(8*N/2)

#doppler vs. time plot
v=ifft(sif)  #now v is a [[]]
vvv=[[20*log(abs(x),10) for x in y]for y in v]
S=[x[:int(len(vvv[0])/2)] for x in vvv]
m=max(max(S))

grid=[[x-m for x in y] for y in S]

#calculate velocity
delta_f = FS/2
lambdaa=c/fc;
velocity = delta_f*lambdaa/2;
#calculate time
time = Tp*len(v)
plt.imshow(grid, extent=[0,velocity,0,time],aspect='auto')
plt.xlim(0,30)
plt.colorbar()
plt.xlabel('Velocity (m/sec)',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('doppler',{'fontsize':20})
plt.tight_layout() 
plt.show()  
