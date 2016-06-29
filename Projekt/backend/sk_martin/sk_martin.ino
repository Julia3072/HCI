#include <Adafruit_NeoPixel.h>
#include <Adafruit_MPR121.h>

// #include <Adafruit_TiCoServo.h>
// #include <known_16bit_timers.h>



// vvvv CapSensor Setup
Adafruit_MPR121 cap = Adafruit_MPR121();

uint16_t lasttouched = 0;
uint16_t currtouched = 0;

// vvv   Neopixel Setup
#define PIN 6
// Parameter 1 = number of pixels in strip
// Parameter 2 = pin number (most are valid)
// Parameter 3 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

int32_t blue = strip.Color(0, 0, 153);
int32_t  green = strip.Color(0, 102, 0);
int32_t  red = strip.Color(255, 0, 0);
int32_t  yellow = strip.Color(255, 255, 0);
int32_t black = strip.Color(0, 0, 0);


void setup() {
  // vvvv CapSensor Setup
  //do not start to early
  while (!Serial);

  Serial.begin(115200);
  Serial.println("Adafruit MPR121 Capacitive Touch sensor test");

   //this will allow the parseInt to read faster and 
  //the arduino board will responsd faster
  Serial.setTimeout(50);   

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
  Serial.print("Thresholds set to "); Serial.print(touch); Serial.print (" and "); Serial.println(rel);

  // vvvv Neopixel Setup
  strip.begin();
  strip.show(); // Initialize all pixels to 'off'
}

//perform Vergleich von indended Touch und gemessenem Touch
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






uint8_t touchedPin() {
  // Get the currently touched pads
  currtouched = cap.touched();
  uint8_t result = 0;

  int threshold_on_alu_things = 150;
  for (uint8_t i = 0; i < 12; i++) {
    if ((cap.filteredData(i) < threshold_on_alu_things) && !(lasttouched & _BV(i))) {
      Serial.println(i);
      result = i;
    }
  }

  // reset our state
  lasttouched = currtouched;

  return result;
}

void setPixels(int from, int to, int32_t color) {

  // flash when range 0
  if (from == to) {
    color = black;
    to = from + 3;
  }

  for (uint16_t i = from; i < to; i++) {
    strip.setPixelColor(i, color);
  }
  strip.show();
}

