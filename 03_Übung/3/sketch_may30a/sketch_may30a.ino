#include <Wire.h>
#include "Adafruit_DRV2605.h"
#include "Adafruit_MPR121.h"

// You can have up to 4 on one i2c bus but one is enough for testing!
Adafruit_MPR121 cap = Adafruit_MPR121();

// Keeps track of the last pins touched
// so we know when buttons are 'released'
uint16_t lasttouched = 0;
uint16_t currtouched = 0;

Adafruit_DRV2605 drv;

void setup() {
  Serial.begin(9600);
  Serial.println("DRV test");
  drv.begin();
  
  drv.selectLibrary(1);
  
  // I2C trigger by sending 'go' command 
  // default, internal trigger when sending GO command
  drv.setMode(DRV2605_MODE_INTTRIG); 

  // ADDRESS TO 3.3 Volt
  if (!cap.begin(0x5B)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
  Serial.println("MPR121 found!");
}

uint8_t effect = 1;

void loop() {

      currtouched = cap.touched();
  
  for (uint8_t i=0; i<12; i++) {
    // it if *is* touched and *wasnt* touched before, alert!
    if ((currtouched & _BV(i)) && !(lasttouched & _BV(i)) ) {
      Serial.print(i); Serial.println(" touched");

      if(i < 4){
          drv.setWaveform(0, 3);  // play effect 
          drv.setWaveform(1, 0);  // end waveform
      } else if (i < 8){
          drv.setWaveform(0, 2);  // play effect 
          drv.setWaveform(1, 0);  // end waveform
      } else {
          drv.setWaveform(0, 1);  // play effect 
          drv.setWaveform(1, 0);  // end waveform
      }

      drv.go();
    }
    // if it *was* touched and now *isnt*, alert!
    if (!(currtouched & _BV(i)) && (lasttouched & _BV(i)) ) {
      Serial.print(i); Serial.println(" released");
    }
  }

  // reset our state
  lasttouched = currtouched;

  // comment out this line for detailed data from the sensor!
  return;
}
