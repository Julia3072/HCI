#include <Adafruit_NeoPixel.h>
#include <Adafruit_MPR121.h>

// #include <Adafruit_TiCoServo.h>
// #include <known_16bit_timers.h>

/* PulseSensor */
//  Variables
int pulsePin = 0;                 // Pulse Sensor purple wire connected to analog pin 0
int blinkPin = 9;                // pin to blink led at each beat
int fadePin = 5;                  // pin to do fancy classy fading blink at each beat
int fadeRate = 0;                 // used to fade LED on with PWM on fadePin

// Volatile Variables, used in the interrupt service routine!
volatile int BPM;                   // int that holds raw Analog in 0. updated every 2mS
volatile int Signal;                // holds the incoming raw data
volatile int IBI = 600;             // int that holds the time interval between beats! Must be seeded!
volatile boolean Pulse = false;     // "True" when User's live heartbeat is detected. "False" when not a "live beat".
volatile boolean QS = false;        // becomes true when Arduoino finds a beat.

// Regards Serial OutPut  -- Set This Up to your needs
static boolean serialVisual = true;   // Set to 'false' by Default.  Re-set to 'true' to see Arduino Serial Monitor ASCII Visual Pulse

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

  pinMode(blinkPin, OUTPUT);        // pin that will blink to your heartbeat!
  pinMode(fadePin, OUTPUT);         // pin that will fade to your heartbeat!
  Serial.begin(115200);             // we agree to talk fast!
  interruptSetup();                 // sets up to read Pulse Sensor signal every 2mS
  // IF YOU ARE POWERING The Pulse Sensor AT VOLTAGE LESS THAN THE BOARD VOLTAGE,
  // UN-COMMENT THE NEXT LINE AND APPLY THAT VOLTAGE TO THE A-REF PIN
  //   analogReference(EXTERNAL);
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

    // pulse sensor
    serialOutput() ;

    if (QS == true) {    // A Heartbeat Was Found
      //Serial.print(BPM);                 // BPM and IBI have been Determined
      // Quantified Self "QS" true when arduino finds a heartbeat
      fadeRate = 255;         // Makes the LED Fade Effect Happen
      // Set 'fadeRate' Variable to 255 to fade LED with pulse
      serialOutputWhenBeatHappens();   // A Beat Happened, Output that to serial.
      QS = false;                      // reset the Quantified Self flag for next time
    }

    ledFadeToBeat();                      // Makes the LED Fade Effect Happen
    delay(20);                             //  take a break
    /********/
    // TODO check for motor update

    int input = Serial.parseInt();

    if (input > 0) {


      //red = 1, green = 2, yellow = 3, blue = 4
      //intensity from 0 to 3 lights activated

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
      Serial.println(i );
      Serial.print( '.' );
      Serial.println(BPM);
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

void ledFadeToBeat() {
  fadeRate -= 15;                         //  set LED fade value
  fadeRate = constrain(fadeRate, 0, 255); //  keep LED fade value from going into negative numbers!
  analogWrite(fadePin, fadeRate);         //  fade LED
}


