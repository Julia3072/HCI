
const int ledPin = 9;      // the pin that the LED is attached to

void setup() {
  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:
  pinMode(ledPin, OUTPUT);
}

void loop() {
  String res;

  if (Serial.available()) {

    int i = 0;
    int brightness = 0;
    while( i < 3){

      int value = (int) (Serial.read() - '0');
      
      if(value >= 0) {
        brightness = brightness * 10 + value;
        i++;
      }
      
    }

    Serial.println(brightness);
    analogWrite(ledPin, brightness);
  }

  delay(2);
}
