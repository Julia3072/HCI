#include <Adafruit_NeoPixel.h>
#include <Adafruit_MPR121.h>

#include <Adafruit_TiCoServo.h>

/* servo */
Adafruit_TiCoServo myservo;
int pos = 0; // variable to store the servo position
int motorPin = 9;

/* CapSensor */
Adafruit_MPR121 cap = Adafruit_MPR121();
uint16_t lasttouched = 0;
uint16_t currtouched = 0;

uint8_t touch = 70;
uint8_t rel = 50;
int threshold_on_faden = 150;

/* Neopixel */
#define PIN 6

Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

int32_t blue = strip.Color(0, 0, 153);
int32_t green = strip.Color(0, 102, 0);
int32_t red = strip.Color(255, 0, 0);
int32_t yellow = strip.Color(255, 255, 0);
int32_t black = strip.Color(0, 0, 0);


void setup() {
  while (!Serial);

  Serial.begin(115200);     
  Serial.setTimeout(50);

  /* CapSensor Setup */
  cap.begin(0x5A);
  cap.setThreshholds(touch,  rel);

  /* Neopixel Setup */
  strip.begin();
  strip.show();

  /* Servo Setup*/
  pinMode(motorPin, OUTPUT);
  myservo.attach(motorPin);
}

void loop() {

  touchedPin();

  if (Serial.available()) {
    int input = Serial.parseInt();

    if (input > 0) {

      if (input >= 100) {

        doReward(input - 100);

      } else {

        //red = 1, green = 2, yellow = 3, blue = 4
        //intensity from 0 to 3 lights activated

        int color = input / 10;
        int intensity = input % 10;

        switch (color) {
          case 1: setPixels(0, 0 + intensity, green); break;
          case 2: setPixels(3, 3 + intensity, red); break;
          case 3: setPixels(6, 6 + intensity, yellow); break;
          case 4: setPixels(9, 9 + intensity, blue); break;
        }
      }
    }
  }
}

/*
    recognize last touched pin and print to serial
*/
void touchedPin() {

  // Get the currently touched pads
  currtouched = cap.touched();

  for (uint8_t i = 0; i < 12; i++) {
    if ((cap.filteredData(i) < threshold_on_faden) && !(lasttouched & _BV(i))) {
      Serial.println(i );
    }
  }

  // reset our state
  lasttouched = currtouched;
}

/*
   update neopixel with range/color
*/
void setPixels(int from, int to, int32_t color) {

  // flash black when nothing to show
  if (from == to) {
    color = black; to = from + 3;
  }

  for (uint16_t i = from; i < to; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

/* reward methods */
void doReward(int percent) {

  for (int i = 0; i < 10; i++) {
    doBlinking(10);
  }

  // 100 percent = 140 degrees
  int deg =  ((float) percent / 100) * 140;

  myservo.write(deg);
  delay(5000);
  myservo.write(0);
}

void doBlinking(int del) {
  setPixels(0, 3, blue);
  delay(del);
  setPixels(3, 6, green);
  delay(del);
  setPixels(6, 9, yellow);
  delay(del);
  setPixels(9, 12, red);
  delay(del);

  setPixels(0, 12, black);
}


