#include <Wire.h>
#include "Adafruit_DRV2605.h"

Adafruit_DRV2605 drv;

void setup() {
  Serial.begin(9600);
  Serial.println("DRV test");
  drv.begin();
  
  drv.selectLibrary(1);
  
  // I2C trigger by sending 'go' command 
  // default, internal trigger when sending GO command
  drv.setMode(DRV2605_MODE_INTTRIG); 

  drv.setWaveform(0, 1);  // play effect 
  drv.setWaveform(1, 0);  // end waveform
}

uint8_t effect = 1;

void loop() {

  if (Serial.available()) {

      int i = 0;
      int brightness = 0;
      while( i < 3){

      int value = (int) (Serial.read() - '0');

      // silly value parsing
      if(value >= 0) {
        brightness = brightness * 10 + value;
        i++;
      }
       }

      Serial.println(brightness);
      if (brightness > 400){

        drv.go();
      } 
    }
}
