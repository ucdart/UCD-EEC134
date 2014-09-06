#Use UART of Raspberry Pi to get fast sampling rate and draw the spectrum
#Cooperate with CY8CKIT-014 from CYPRESS to reach sampling rate at 40kHz
#written by Meng Wei, a summer exchange student (UCD GREAT Program, 2014) from Zhejiang University, China

import serial
import time
import pylab as plt
from numpy import linspace
from numpy.fft import fft

port= serial.Serial("/dev/ttyAMA0",baudrate=115200,timeout=1.0)
data=raw_input("Reconnect Raspberry Pi header:")#the system is not very stable
#when it doesn't work you need to reconnect RPi or CYPRESS to get restart

port.write('A07FF')
print(port.inWaiting())
samples=port.read(2048)
s= map(ord,samples)
print len(s)
Y=fft(s)
frq=linspace(0,40000,len(Y))
plt.plot(frq,abs(Y),'r') # plotting the spectrum
plt.xlabel('Freq (Hz)')
plt.ylabel('|Y(freq)|')
plt.show()
