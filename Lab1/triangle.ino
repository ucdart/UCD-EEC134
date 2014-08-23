/*
Triangle wave and sync pulse generator to control a (0-5V input range) VCO for FMCW radar.
The MPC4921 DAC is used to generate a triangle wave with a period of 40ms.
PWM of the Arduino UNO is use to simultaneously generate the sync pulse,
used for signal processing.


*/

#include "SPI.h" // SPI library for communicating with the DAC 
byte data = 0;// A byte is an 8-bit number
word outputValue = 0;// A word is a 16-bit number

void setup()
{
    // Set pins for input and output
    pinMode(8, OUTPUT);                     // SYNC pin
    pinMode(10, OUTPUT);                    // Slave-select (SS) pin
    SPI.setClockDivider(SPI_CLOCK_DIV2);    // Set the SPI clock to 8MHz
    SPI.begin();                            // Activate the SPI bus
    SPI.setBitOrder(MSBFIRST);              // Most significant bit first for MCP4921
}

void loop()
{
    digitalWrite(8, HIGH);              // SYNC pulse high
    
    // Rising edge of the triangle wave
    for (int a = 0; a <= 4080; a=a+4)   
    {
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
    for (int a = 4080; a >= 4; a = a-4) 
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
