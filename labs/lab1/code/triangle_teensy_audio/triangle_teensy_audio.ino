/*
Triangle wave and sync pulse generator to control a (0-5V input range) VCO for FMCW radar.
The MPC4921 DAC is used to generate a triangle wave with a period of 40ms.
PWM of the Arduino UNO is use to simultaneously generate the sync pulse,
used for signal processing.


*/
#include <Audio.h>
#include <Wire.h>
#include <SPI.h>
#include <SD.h>

// GUItool: begin automatically generated code
AudioSynthWaveform       waveform1;      //xy=311,279
AudioOutputAnalog        dac1;           //xy=689,277
AudioConnection          patchCord1(waveform1, dac1);
// GUItool: end automatically generated code

void setup()
{
  AudioMemory(16);
  waveform1.begin(0.75, 4000, WAVEFORM_TRIANGLE);
}

void loop()
{

}
