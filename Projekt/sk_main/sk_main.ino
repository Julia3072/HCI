#include <Adafruit_NeoPixel.h>
#include <Adafruit_MPR121.h>

// #include <Adafruit_TiCoServo.h>
// #include <known_16bit_timers.h>

/* CapSensor */
Adafruit_MPR121 cap = Adafruit_MPR121();
uint16_t lasttouched = 0;
uint16_t currtouched = 0;

uint8_t touch = 70;
uint8_t rel = 50;
int threshold_on_alu_things = 150;

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
}

void loop() {

  touchedPin();

  if (Serial.available()) {

    // TODO check for motor update

    int input = Serial.parseInt();

    if (input > 0) {

      /*
         red = 1, green = 2, yellow = 3, blue = 4
         intensity from 0 to 3 lights activated
      */
      int color = input / 10;
      int intensity = input % 10;

      switch (color) {
        case 1: setPixels(0, 0 + intensity, red); break;
        case 2: setPixels(3, 3 + intensity, green); break;
        case 3: setPixels(6, 6 + intensity, yellow); break;
        case 4: setPixels(9, 9 + intensity, blue); break;
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
    if ((cap.filteredData(i) < threshold_on_alu_things) && !(lasttouched & _BV(i))) {
      Serial.println(i);
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

