# -*- coding: utf-8 -*-
# Real-time Doppler speed calculation and display 
# using the computer sound card as input
# 
#originally written by Meng Wei, a summer exchange student (UCD GREAT Program, 2013) from Zhejiang University, China
#modified by Xiaoguang Liu (lxgliu@ucdavis.edu) Sept 2015
#Modified by Abdullah Sairafi September 2018
#To Do:
# - Add GUI guide for selecting the sound input device
# - 

#import pyaudio
import numpy as np
import math
import time
import sys
from matplotlib import pyplot as plt
from struct import unpack
from matplotlib.widgets import Button
from ctypes import *

# FFT function
def fftlogmag(data):
    '''
    compute log magnitude of the fft of data
    '''
    o=20*np.log10(np.absolute(np.fft.fft(data))+1e-10)  #add a small number 1e-10 to avoid divide by zero
    
	#only the first half in each row contains unique information
    return o[:int(len(o)/2)]

# Library for Analog Discovery
if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#declare ctype variables
hdwf = c_int()
sts = c_byte()
frequency = c_double(100000) # frequency of acquisition 
nSamples = 500 #size of the buffer to put the current acquisition
rgdSamples = (c_double*nSamples)() #the raw data 
cValid = c_int(0)

s=np.zeros(nSamples, dtype=int)
v=s

#set up display
#create figure
fig=plt.figure()

#time domain signal plot
ax1 = fig.add_subplot(2,1,1)
lines_time = ax1.plot(s)
plt.xlim([0, int(nSamples)])
plt.ylim([1.5, 2.5])
t=range(0,9)     #8 major ticks
xticks=[x*nSamples/8 for x in t]
ax1.set_xticks(xticks)

#frequency domain signal display
ax2 = fig.add_subplot(2,1,2)
lines_freq=ax2.plot(v,'b')

plt.xlim([0, int(nSamples/2)])
t=range(0,9)     #8 major ticks
xticks=[x*nSamples/16 for x in t]

#scale the tick labels to the proper speed
xtick_labels=[str(int(x*frequency.value/8)) for x in t]
ax2.set_xticks(xticks)
ax2.set_xticklabels(xtick_labels)

plt.xlabel('Frequency (Hz)',{'fontsize':12})
plt.ylabel('time [s]',{'fontsize':12})


#open Analogdiscovery

print "Opening first device"
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == 0:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print szerr.value
    print "failed to open device"
    quit()

#set up acquisition
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, c_int(1)) #acqmodeScanShift
dwf.FDwfAnalogInFrequencySet(hdwf, frequency)
dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(nSamples))

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

#begin acquisition
dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))


#add a stop button
#press the stop button to stop the program

STOP = False
def Stop(event):
    global STOP 
    #STOP = not STOP
    print("ending program")
    quit()

ax_stop = fig.add_axes([0.8, 0.01, 0.1, 0.05])
bn_stop = Button(ax_stop, 'Stop', color='0.65')
bn_stop.on_clicked(Stop)

plt.ion()
plt.show()

while not STOP:
    lines_time.pop(0).remove()
    lines_freq.pop(0).remove()
    
    #Functions to read data from analog discovery
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    dwf.FDwfAnalogInStatusSamplesValid(hdwf, byref(cValid))
    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgdSamples), cValid) # get channel 1 data
    
    v=fftlogmag(rgdSamples)

    lines_time=ax1.plot(rgdSamples,'b')     #time domain signal plot
    lines_freq=ax2.plot(v,'b')     #frequency domain signal plot
    
    plt.draw()
    plt.pause(0.01)