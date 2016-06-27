#include <Wire.h>
#include "Adafruit_MPR121.h"

Adafruit_MPR121 cap = Adafruit_MPR121();

uint16_t lasttouched = 0;
uint16_t currtouched = 0;

void setup() {
   //do not start to early
  while (!Serial);
        
  Serial.begin(9600);
  Serial.println("Adafruit MPR121 Capacitive Touch sensor test"); 
  
  // Default address is 0x5A, if tied to 3.3V its 0x5B
  // If tied to SDA its 0x5C and if SCL then 0x5D
  if (!cap.begin(0x5A)) {
    Serial.println("MPR121 not found, check wiring?");
    while (1);
  }
  Serial.println("MPR121 found!");
  
  uint8_t touch = 70;
  uint8_t rel = 50;
   cap.setThreshholds( touch,  rel);
  Serial.print("Thresholds set to ");Serial.print(touch); Serial.print (" and "); Serial.println(rel);
}

void loop() {
  // Get the currently touched pads
  currtouched = cap.touched();
  
  int threshold_on_alu_things = 100;
  for(uint8_t i=0; i<12; i++){
    if ((cap.filteredData(i) <threshold_on_alu_things) && !(lasttouched & _BV(i))){ 
      Serial.println(i);}
    }

  // reset our state
  lasttouched = currtouched;

  return;
}
