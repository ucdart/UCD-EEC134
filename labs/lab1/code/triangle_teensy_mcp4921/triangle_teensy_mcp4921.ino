/*
Triangle wave and sync pulse generator to control a (0-5V input range) VCO for FMCW radar.
The MPC4921 DAC is used to generate a triangle wave with a period of 40ms.
PWM of the Arduino UNO is use to simultaneously generate the sync pulse,
used for signal processing.


*/

#include <SPI.h> // Include the SPI library 

word outputValue = 4;// A word is a 16-bit number
int incr = 4;

const int slaveSelectPin = 10; //set the slave select (chip select) pin number
const int SYNC = 8;  //set the SYNC output pin number
 
void setup()
{
    // Set pins for output
    pinMode(SYNC, OUTPUT);                     // SYNC pin
    digitalWrite(SYNC, LOW);               // Sync pulse low
    pinMode(slaveSelectPin, OUTPUT);                    // Slave-select (SS) pin
    SPI.begin();                            // Activate the SPI bus
    SPI.beginTransaction(SPISettings(16000000, MSBFIRST, SPI_MODE0));  // Set up the SPI transaction; this is not very elegant as there is never a close transaction action.
}

void loop()
{


    if (outputValue == 4092 || outputValue == 0){
      incr = -incr;
      digitalWrite(SYNC, !digitalRead(SYNC));
    }
    
    outputValue = outputValue + incr;

    byte HighByte =highByte(outputValue);    // Take the upper byte
    HighByte = 0b00001111 & HighByte;       // Shift in the four upper bits (12 bit total)
    HighByte = 0b00110000 | HighByte;       // Keep the Gain at 1 and the Shutdown(active low) pin off
    byte LowByte = lowByte(outputValue);     // Shift in the 8 lower bits
    
    digitalWrite(slaveSelectPin, LOW);          
    SPI.transfer(HighByte);            // Send the upper byte
    SPI.transfer(LowByte);             // Send the lower byte
    digitalWrite(slaveSelectPin, HIGH);         // Turn off the SPI transmission
}
