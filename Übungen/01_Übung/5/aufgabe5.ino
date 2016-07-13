int potPin = 1; // Potentiometer output connected to analog pin 3
int potVal = 0; // Variable to store the input from the potentiometer


void setup() 
{
//initialize serial communications at a 9600 baud rate
Serial.begin(9600);
}

void loop()
{
//send 'Hello, world!' over the serial port

potVal = analogRead(potPin);   // read the potentiometer value at the input pin
Serial.println(potVal);

//wait 100 milliseconds so we don't drive ourselves crazy
delay(100);
}

