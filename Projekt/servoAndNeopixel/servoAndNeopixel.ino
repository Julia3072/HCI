
#include <Adafruit_TiCoServo.h>

#include <Adafruit_NeoPixel.h>

// servo vars
Adafruit_TiCoServo myservo;
int pos = 0; // variable to store the servo position
int motorPin = 9;

int add = 0;

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

  strip.begin();
  strip.show(); // Initialize all pixels to 'off'

  pinMode(motorPin, OUTPUT);
  myservo.attach(motorPin);
  Serial.begin(9600);

}
void loop() {
  // percentage of reward
  doReward(100);
}

void doReward(int percent) {
  // 100 percent = 140 degrees
  int maxDegrees = 140;
  int deg =  ((float)percent / 100) * maxDegrees;
  doUp(deg);
  delay(2000);
  if (percent = 100) {
    doBlinking(1000);
  }
  for (int i = 0; i < 10; i++) {
    doBlinking(10);
  }

  delay(2000);
  doDown(deg);
  delay(2000);
}

void doBlack() {
  for (uint16_t i = 0; i < 12; i++) {
    strip.setPixelColor(i, black);
    strip.show();
  }

}

void doUp(int to) {
  Serial.write("doUp()");

  for (pos = 0; pos < to; pos += 1)
  {
    myservo.write(pos); // tell servo to go to position in variable 'pos'
    delay(15); // waits 15ms for the servo to reach the position
  }


}

void doDown(int from) {
  Serial.write("doDown()");

  for (pos = from; pos >= 1; pos -= 1) // goes from 180 degrees to 0 degrees
  {
    myservo.write(pos); // tell servo to go to position in variable 'pos'
    delay(15); // waits 15ms for the servo to reach the position
  }

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

  doBlack();

}

void setPixels(int from, int to, int32_t color) {

  for (uint16_t i = from; i < to; i++) {
    strip.setPixelColor(i, color);
    strip.show();
    delay(10);
  }

}
