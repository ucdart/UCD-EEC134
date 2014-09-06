# -*- coding: utf-8 -*-
#Real Time Doppler Radar
#written by Meng Wei, a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China

import spidev
from numpy.fft import ifft
from math import log
import pylab as plt

#constants
c=3E8 #(m/s) speed of light

#radar parameters
FS = 5600#Sampling rate with SPI port
Tp = 0.1#(s) pulse time
N = 2000# of samples per pulsRe
fc = 2590E6;#(Hz) Center frequency (connected VCO Vtune to +5)

delta_f = FS/2
lambdaa=c/fc
velocity = delta_f*lambdaa/2
Time = 1
#talk to SPI
spi=spidev.SpiDev()
spi.open(0,0)

fig=plt.figure()
plt.ion()
plt.show()

for i in range(10):
    plt.cla()
    for k in range(5000):#This loop takes nearly 1 sec
        r=spi.xfer2([1,8<<4,0],16000000,0)
        s.append((((r[1]&3)<<8)+r[2]))
   
    sif=[]
    for ii in range(1,int(round(len(s)/N))):
             sif.append(s[int((ii-1)*N):int(ii*N)])
    me=sum(s)/len(s)
    sif = [[x - me for x in y]for y in sif]
    v=ifft(sif)  #now v is a [[]]
    vvv=[[20*log(abs(x),10) for x in y]for y in v]
    S=[x[:int(len(vvv[0])/2)] for x in vvv]
    m=max(max(bufferVel))
    grid=[[x-m for x in y] for y in bufferVel]             

    plt.imshow(grid, extent=[0,velocity,0,Time],aspect='auto')
    plt.xlim(0,5)
    plt.xlabel('Velocity (m/sec)',{'fontsize':20})
    plt.ylabel('time [s]',{'fontsize':20})
    plt.title('real_time_doppler',{'fontsize':20})
    plt.draw()
   
