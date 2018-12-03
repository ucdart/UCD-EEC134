"""
   Adapted from:
   DWF Python Example
   Author:  Digilent, Inc.
   Revision: 10/17/2013

   Requires:
       Python, numpy, matplotlib
"""
from ctypes import *
from dwfconstants import *
import math
import matplotlib.pyplot as plt
import numpy as np
import sys
import time

#def format_divide_by_1000(value, tick_number):
#    return int(value/1000)

#detect OS and set the right PATH for dwf libraries
if sys.platform.startswith("win"):
    dwf = cdll.dwf
elif sys.platform.startswith("darwin"):
    dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
else:
    dwf = cdll.LoadLibrary("libdwf.so")

#operation parameters
freqS = 50000   # sampling frequency (Hz) (in python native variable)
tSampling = 5  #sampling time length (s) in python native variable
nSamples = freqS*tSampling   # number of total samples

#declare ctype variables
hdwf = c_int()  #hardware handle for the AD devices
sts = c_byte()  #state variable
hzAcq = c_double(freqS) #sampling frequency in Hz in ctype
rgdSamples = (c_double*nSamples)()  #array to store sampled data from channel 1
rgdSamples_ch2 = (c_double*nSamples)()  #array to store sampled data from channel 1
cAvailable = c_int()
cLost = c_int()
cCorrupted = c_int()
fLost = 0
fCorrupted = 0

#print DWF version
version = create_string_buffer(16)
dwf.FDwfGetVersion(version)
print("DWF Version: "+version.value.decode("ascii"))

#open device
print("Opening Analog Discovery #0")
dwf.FDwfDeviceOpen(c_int(-1), byref(hdwf))

if hdwf.value == hdwfNone.value:
    szerr = create_string_buffer(512)
    dwf.FDwfGetLastErrorMsg(szerr)
    print(szerr.value)
    print("failed to open device")
    quit()

print("Preparing to read sample...")

#set up acquisition
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(0), c_bool(True))  #enable channel 1
dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(1), c_bool(True))  #enable channel 2
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(0), c_double(5))    #set channel 1 measurement range to 5V
dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(1), c_double(5))    #set channel 1 measurement range to 5V
dwf.FDwfAnalogInAcquisitionModeSet(hdwf, acqmodeRecord) #set operation mode to record
dwf.FDwfAnalogInFrequencySet(hdwf, hzAcq)   #set the sampling frequency
#dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(nSamples/hzAcq.value)) # -1 infinite record length
dwf.FDwfAnalogInRecordLengthSet(hdwf, c_double(tSampling)) # -1 infinite record length

#wait at least 2 seconds for the offset to stabilize
time.sleep(2)

#begin acquisition
dwf.FDwfAnalogInConfigure(hdwf, c_int(0), c_int(1))
print("   waiting to finish")

#samples data
cSamples = 0

while cSamples < nSamples:
    dwf.FDwfAnalogInStatus(hdwf, c_int(1), byref(sts))
    if cSamples == 0 and (sts == DwfStateConfig or sts == DwfStatePrefill or sts == DwfStateArmed) :
        # Acquisition not yet started.
        continue

    dwf.FDwfAnalogInStatusRecord(hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))

    cSamples += cLost.value

    if cLost.value :
        fLost = 1
    if cCorrupted.value :
        fCorrupted = 1

    if cAvailable.value==0 :
        continue

    if cSamples+cAvailable.value > nSamples :
        #cAvailable = c_int(nSamples-cSamples)
        break

    dwf.FDwfAnalogInStatusData(hdwf, c_int(0), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 1 data
    dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(rgdSamples_ch2, sizeof(c_double)*cSamples), cAvailable) # get channel 2 data
    cSamples += cAvailable.value

print("Recording finished")
if fLost:
    print("Samples were lost! Reduce frequency")
if fCorrupted:
    print("Samples could be corrupted! Reduce frequency")

#close the device handle
dwf.FDwfDeviceClose(hdwf)
print("Device closed.")

#data processing
data = np.zeros((len(rgdSamples), 2))
data[:,0]=rgdSamples
data[:,1]=rgdSamples_ch2

#saving the data in a text file
np.savetxt('recording.dat', data, delimiter=', ')

#plot the sampled data
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(7, 10))  # createa 3-row 1-column plot. Figure size in inches.

axes[0].plot(data[:,0])   # plot channel 1 data
axes[0].set_title("Channel 1")
axes[0].set_xlabel('Samples')
axes[0].set_xlim([0,250000])
axes[0].set_ylabel('Voltage (V)')

axes[1].plot(data[:,1])   # plot channel 2 data
axes[1].set_title("Channel 1")
axes[1].set_xlabel('Samples')
axes[1].set_xlim([0,250000])
axes[1].set_ylabel('Voltage (V)')

axes[2].magnitude_spectrum(data[:,0], Fs=freqS, scale='dB')   # plot spectrum of channel 1 data
axes[2].set_title("Log. Magnitude Spectrum")
axes[2].set_xlabel('Frequency (Hz)')
axes[2].set_xlim([0,25000])
#axes[2].set_xlabel('Frequency (Hz)')
#axes[2].xaxis.set_major_formatter(plt.FuncFormatter(format_divide_by_1000))

fig.tight_layout()  #fit all subplots nicely into the figure
