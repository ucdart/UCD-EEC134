# -*- coding: utf-8 -*-
#range radar, reading files from a WAV file
#Written by Meng Wei, a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China


import wave
from struct import unpack
from numpy.fft import ifft
import matplotlib.pyplot as plt 
from math import log

#read the raw data .wave file here
wavefile = wave.open(r"D:\Michealia Wei\MIT_OCW_notes\ranging_files\ranging_files\running_outside_20ms.wav", "rb")
nchannels = wavefile.getnchannels()
sample_width = wavefile.getsampwidth()
framerate = wavefile.getframerate()
numframes = wavefile.getnframes()

trig = []
s=[]
for i in range(numframes):
    val = wavefile.readframes(1)
    left = val[0:2]
    right = val[2:4]
    v = unpack('h', left )[0]
    u = unpack('h', right )[0]
    trig.append((v+2**15-32768)*-1.0/32768.0)
    s.append((u+2**15-32768)*-1.0/32768.0)

#constants
c = 3E8 #(m/s) speed of light

#radar parameters
Tp = 20E-3 #(s) pulse time
FS=framerate
N = Tp*FS  ## of samples per pulse
fstart = 2260E6 #(Hz) LFM start frequency
fstop = 2590E6 #(Hz) LFM stop frequency
BW = fstop-fstart #(Hz) transmti bandwidth

#range resolution
rr = c/(2*BW)
max_range = rr*N/2


#parse the data here by triggering off rising edge of sync pulse
count = 0
thresh = 0
sif=[]
start = [x>thresh for x in trig]
for ii in range(100,int(len(start)-N)+1):
    mean=sum(start[ii-12:ii-1])*1.0/11.0
    if start[ii-1]==1 and mean==0:
        count=count+1
        sif.append(s[ii-1:int(ii+N-1)])
T=(len(start)-N)/FS

#subtract the average
M=int(len(sif))
s_T=[[sif[j][i] for j in range(M)] for i in range(int(N))]#this line is time consuming!

for k in range(int(N)):
    ave=sum(s_T[k])/M
    for d in range(M):
        sif[d][k]=sif[d][k]-ave

zpad = int(8*N/2)

#RTI plot
v=ifft(sif,zpad,1)  #now v is a [[]]
vvv=[[20*log(abs(x),10) for x in y]for y in v]
S=[x[:int(len(vvv[0])/2)] for x in vvv]
m=max(max(vvv))
grid=[[x-m for x in y] for y in S]

plt.imshow(grid, extent=[0,max_range,0,T],aspect='auto')
plt.colorbar()
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI without clutter rejection',{'fontsize':20})
plt.tight_layout() 
plt.show()

#2 pulse cancelor RTI plot
p=sif[1:M]
q=sif[0:M-1]
sif2=[]
for i in range(M-1):
    sif2.append(map(float.__sub__, p[i], q[i]))
v=ifft(sif2,zpad,1)
vvv=[[20*log(abs(x),10) for x in y]for y in v]
S=[x[:int(len(vvv[0])/2)] for x in vvv]
m=max(max(S))
grid=[[x-m for x in y] for y in S]
plt.imshow(grid, extent=[0,max_range,0,T],aspect='auto')
plt.colorbar()
plt.xlabel('Range[m]',{'fontsize':20})
plt.ylabel('time [s]',{'fontsize':20})
plt.title('RTI with 2-pulse cancelor clutter rejection',{'fontsize':20})
plt.tight_layout()  
plt.show()
