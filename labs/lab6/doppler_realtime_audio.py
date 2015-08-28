# -*- coding: utf-8 -*-
# Real-time Doppler speed calculation and display 
# using the computer sound card as input
# 
#originally written by Meng Wei, a summer exchange student (UCD GREAT Program, 2013) from Zhejiang University, China
#modified by Xiaoguang Liu (lxgliu@ucdavis.edu) in Aug.2015

import pyaudio
import numpy as np
from numpy.fft import fft
from math import log
from matplotlib import pyplot as plt
from struct import unpack
from matplotlib.widgets import Button

def fftlogmag(data):
    '''
    computer log magnitude of the fft of data
    '''
    o=[20*log(abs(x),10) for x in fft(data)]
    #only the first half in each row contains unique information
    return o[:int(len(o)/2)]

#constants
c=3E8 #(m/s) speed of light

CHUNK = 2048
FORMAT = pyaudio.paInt16     #16-bit
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 10

#radar parameters
fc = 2590E6  #(Hz) Center frequency (connected VCO Vtune to +5)
wavelength = c/fc

f_max = RATE/2    #maximum frequency that can be measured; Nyquist criteria
v_max = f_max*wavelength/2

s=np.random.rand(CHUNK)
v=s

#set up display
fig=plt.figure()

#time domain signal plot
ax1 = fig.add_subplot(2,1,1)
lines_time = ax1.plot(s)
plt.xlim([0, int(CHUNK)])
t=range(0,9)     #8 major ticks
xticks=[x*CHUNK/8 for x in t]
ax1.set_xticks(xticks)

#frequency domain signal display
ax2 = fig.add_subplot(2,1,2)
lines_freq=ax2.plot(v,'b')

plt.xlim([0, int(CHUNK/2)])
t=range(0,9)     #8 major ticks
xticks=[x*CHUNK/16 for x in t]
#scale the tick labels to the proper speed
xtick_labels=[str(int(x*v_max/8)) for x in t]
ax2.set_xticks(xticks)
ax2.set_xticklabels(xtick_labels)

plt.xlabel('Velocity (m/sec)',{'fontsize':12})
plt.ylabel('time [s]',{'fontsize':12})

#add a stop button
#press the stop button to stop the program
STOP = False
def Stop(event):
    global STOP 
    STOP = not STOP

ax_stop = fig.add_axes([0.8, 0.01, 0.1, 0.05])
bn_stop = Button(ax_stop, 'Stop', color='0.65')
bn_stop.on_clicked(Stop)

plt.ion()
plt.show()

#set up audio input
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while not STOP:
    lines_time.pop(0).remove()
    #psd_lines.pop(0).remove()
    lines_freq.pop(0).remove()
    
    data = stream.read(CHUNK)
    
    for i in range(0,CHUNK):
        #get the right channel
        right = data[4*i+2:4*i+4]
        #.wav file store the sound level information in signed 16-bit integers stored in little-endian format
        #The "struct" module provides functions to convert such information to python native formats, in this case, integers.
        u = unpack('h', right)[0]            
        #normalize the value to 1 and store them in a two dimensional array "s"        
        s[i]=u/32768.0
    
    v=fftlogmag(s)
  
    lines_time=ax1.plot(s,'b')     #time domain signal plot
    lines_freq=ax2.plot(v,'b')     #frequency domain signal plot
    
    plt.draw()
    plt.pause(0.01)
