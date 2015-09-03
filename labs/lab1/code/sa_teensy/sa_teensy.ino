//Code modified from https://dl.dropboxusercontent.com/u/4088422/TeensySA.ino
//A video demo of the original project by rheslip20@Youtube

#include <Audio.h>
#include <Wire.h>
#include <SD.h>

#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library
#include <SPI.h>

//Set up Teensy SPI connections and Pins for interfacing with the 1.8" 128 X 160 TFT LCD display
#define sclk 5  // connect to LCD Pin 5-CLK (SPI clock
#define mosi 4  // connect to LCD Pin 4-DIN (master data out slave data in)
#define dc   3  // connect to LCD Pin 3-d/c
#define cs   2  // connect to LCD Pin 2-cs (chip select)
#define rst  1  // connect to LCD Pin 1-RST (reset)

// It should also be possible to use HW SPI interface for TFT
//Adafruit_S6D02A1 tft = Adafruit_S6D02A1(cs, dc, rst);

// Set up soft-SPI interface for the display
Adafruit_ST7735 tft = Adafruit_ST7735(cs, dc, mosi, sclk, rst);

// Create the Audio components.  These should be created in the
// order data flows, inputs/sources -> processing -> outputs

// Waveform synthesizer for triangle wave generation
AudioSynthWaveform       waveform1;      

//Create the sampling components
AudioOutputAnalog     dac1;       // Set up triangle wave output through the DAC
AudioInputAnalog      adc1(A1);   // Set up Teensy pin A1 for ADC input
AudioAnalyzeFFT1024   myFFT;      // Set up 1024-point FFT

// Create Audio connections between the components
AudioConnection       c1(waveform1, dac1);
AudioConnection       c2(adc1, myFFT);

void setup() {

  // Audio connections require memory to work.  For more
  // detailed information, see the MemoryAndCpuUsage example
  AudioMemory(12);

  // Set up the triangle wave synthesizer. 
  // The first argument is amplitude, second frequency, and the third waveform type
  // Refer to the source code for information: https://github.com/PaulStoffregen/Audio/blob/master/synth_waveform.cpp
  waveform1.begin(0.25, 4000, WAVEFORM_TRIANGLE);
 
  // If your TFT's plastic wrap has a Black Tab, use the following:
  //tft.initR(INITR_BLACKTAB);   // initialize a S6D02A1S chip, black tab
  // If your TFT's plastic wrap has a Red Tab, use the following:
  //tft.initR(INITR_REDTAB);   // initialize a S6D02A1R chip, red tab
  // If your TFT's plastic wrap has a Green Tab, use the following:
  tft.initR(INITR_GREENTAB); // initialize a S6D02A1R chip, green tab
  
  tft.setRotation(1);
  Serial.println("init");
  
  uint16_t time = millis();
  tft.fillScreen(ST7735_BLACK);
  time = millis() - time;
  Serial.println(time, DEC);

  // large block of text
  tft.fillScreen(ST7735_BLACK);
  tft.setCursor(0, 115);
  tft.setTextColor(ST7735_WHITE);
  tft.setTextWrap(true);
  tft.print("Teensy Spectrum Analyser 2");
  Serial.println("Set up screen complete");

 // pin 21 will select rapid vs animated display
  pinMode(21, INPUT_PULLUP);
}

int count=0;
const int nsum[16] = {1, 1, 2, 2, 3, 4, 5, 6, 6, 8, 12, 14, 16, 20, 28, 24};
int peak[512];
int maximum[16];
unsigned long last_time = millis();

void loop() {
  //while(1);
  Serial.println("start");
  if (myFFT.available()) {
    //Serial.println("FFT completed.");

    // The display scale is currently hard-coded into the code
    int scale = 16;
    
    //  A better alternative is to implement an adjustable scale by a potentiometer connected to an analog input A2
    
    // graphing the bars for the spectrum display
    for (int16_t x=0; x < 160; x+=1) {
      //tft.drawFastVLine(x, 0, myFFT.output[x]/scale, S6D02A1_GREEN);
           int bar=abs(myFFT.output[x])/scale;
           if (bar >110) bar=110;
           if (bar > peak[x]) peak[x]=bar;
           tft.drawFastVLine(x, 110-bar,bar, ST7735_MAGENTA);
      //     tft.drawFastVLine(x+1, 20, abs(myFFT.output[x]/scale), S6D02A1_GREEN);
           tft.drawFastVLine(x, 0, 110-bar, ST7735_BLACK);    
      //     tft.drawFastVLine(x+1, 20+abs(myFFT.output[x]/scale), 80, S6D02A1_BLACK); 
           tft.drawPixel(x,110-peak[x], ST7735_YELLOW);
      //     tft.drawFastVLine(x, 110-peak[x],bar, S6D02A1_BLUE);    
           if(peak[x]>0) peak[x]-=5;
    }
    Serial.println("Display updated.");
 
    // Change this to if(1) for measurement output
    if(0) {
    /*
      For PlaySynthMusic this produces:
      Proc = 20 (21),  Mem = 2 (8)
    */
      if(millis() - last_time >= 5000) {
        Serial.print("Proc = ");
        Serial.print(AudioProcessorUsage());
        Serial.print(" (");    
        Serial.print(AudioProcessorUsageMax());
        Serial.print("),  Mem = ");
        Serial.print(AudioMemoryUsage());
        Serial.print(" (");    
        Serial.print(AudioMemoryUsageMax());
        Serial.println(")");
        last_time = millis();
      }
    } 
  }
}


