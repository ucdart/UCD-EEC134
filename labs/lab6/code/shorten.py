# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 21:57:49 2015

@author: Xiaoguang
"""
import os
import wave

#read the raw data .wave file here
#get path to the .wav file
filename = os.getcwd() + '\\running_outside_20ms.wav'
ofilename = os.getcwd() + '\\output.wav'
#open .wav file
wavefile = wave.open(filename, "rb")
owavefile = wave.open(ofilename,'w')
# number of channels
nchannels = wavefile.getnchannels()
owavefile.setnchannels(nchannels)

# number of bits per sample
sample_width = wavefile.getsampwidth()
owavefile.setsampwidth(sample_width)

#print(sample_width)

# sampling rate
Fs = wavefile.getframerate()
owavefile.setframerate(Fs)
#print(Fs)

# number of samples per pulse
#N = int(Tp*Fs)  ## of samples per pulse

#range resolution
#rr = c/(2*BW)

# number of frames (total samples)
numframes = wavefile.getnframes()

#number of rows
#rows = int(numframes/N)

# trig stores the sampled data in the .wav file
#trig =np.zeros([rows,N])
# s stores the sampled data in the .wav file
#s =np.zeros([rows,N])

for i in range(int(numframes/6)):
    data = wavefile.readframes(1)
    owavefile.writeframes(data)
