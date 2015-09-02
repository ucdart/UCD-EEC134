/*
Triangle wave and sync pulse generator to control a (0-5V input range) VCO for FMCW radar.
The MPC4921 DAC is used to generate a triangle wave with a period of 40ms.
PWM of the Arduino UNO is use to simultaneously generate the sync pulse,
used for signal processing.


*/

#include <SPI.h> // Include the SPI library 
byte data = 0;// A byte is an 8-bit number
word outputValue = 0;// A word is a 16-bit number
const int slaveSelectPin = 10; //set the slave select (chip select) pin number
const int Sync = 8  //set the SYNC output pin number
void setup()
{
    // Set pins for output
    pinMode(Sync, OUTPUT);                     // SYNC pin
    pinMode(slaveSelectPin, OUTPUT);                    // Slave-select (SS) pin
    SPI.begin();                            // Activate the SPI bus
}

void loop()
{
    digitalWrite(8, HIGH);              // SYNC pulse high

    a = 4;
    incr = 4;
    // Rising edge of the triangle wave
    while (1)
    {
        if (a = 4092 | a = 0){
          incr = -incr;
        }
        // gain control of the SPI port
        // and configure settings
        SPI.beginTransaction(SPISettings(8000000, LSBFIRST, SPI_MODE0));
        outputValue = a;
        digitalWrite(10, LOW);          // Activate the the SPI transmission
        data =highByte(outputValue);    // Take the upper byte
        data = 0b00001111 & data;       // Shift in the four upper bits (12 bit total)
        data = 0b00110000 | data;       // Keep the Gain at 1 and the Shutdown(active low) pin off
         SPI.transfer(data);            // Send the upper byte
        data =lowByte(outputValue);     // Shift in the 8 lower bits
        SPI.transfer(data);             // Send the lower byte
        digitalWrite(10, HIGH);         // Turn off the SPI transmission
    }
  
    digitalWrite(8, LOW);               // Sync pulse low
    
    // Falling edge of the triangle wave, very similar as above
    for (int a = 4092; a >= 4; a = a-4) 
    {
        outputValue = a;
        digitalWrite(10, LOW);
        data =highByte(outputValue);
        data = 0b00001111 & data;
        data = 0b00110000 | data;
        SPI.transfer(data);
        data =lowByte(outputValue);
        SPI.transfer(data);
        digitalWrite(10, HIGH);
    }
}
