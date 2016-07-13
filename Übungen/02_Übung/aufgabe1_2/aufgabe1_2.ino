
#include <Servo.h>

// servo vars
Servo myservo;
int pos = 0; // variable to store the servo position
int motorPin = 3;

int redLed = 5;
int yellowLed = 6;
int greenLed = 7;

// sensor vars
long duration;
int distance;
const int trigPin = 9;
const int echoPin = 10;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(motorPin, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);
  pinMode(greenLed, OUTPUT);

  myservo.attach(motorPin);
  Serial.begin(9600);

}
void loop() {

  digitalWrite(redLed, HIGH);

  if ( getDistance() <= 100) {
    doAmpel();
  }

}

void doAmpel() {
  delay(2000);
  digitalWrite(yellowLed, HIGH);
  delay(2000);

  digitalWrite(greenLed, HIGH);
  
  digitalWrite(redLed, LOW);
  digitalWrite(yellowLed, LOW);
  doSchrankeAuf();
  delay(5000);

  digitalWrite(greenLed, LOW);
  digitalWrite(yellowLed, HIGH);
  delay(2000);
  doSchrankeZu();
  digitalWrite(yellowLed, LOW);
  digitalWrite(redLed, HIGH);
}

int getDistance() {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH);

  distance = duration * 0.034 / 2;

  Serial.print("Distance: ");
  Serial.println(distance);

  return distance;
}

void doSchrankeAuf() {


  for (pos = 0; pos < 90; pos += 1) 
  {
    myservo.write(pos); // tell servo to go to position in variable 'pos'
    delay(15); // waits 15ms for the servo to reach the position
  }


}

void doSchrankeZu() {

  for (pos = 90; pos >= 1; pos -= 1) // goes from 180 degrees to 0 degrees
  {
    myservo.write(pos); // tell servo to go to position in variable 'pos'
    delay(15); // waits 15ms for the servo to reach the position
  }

}
