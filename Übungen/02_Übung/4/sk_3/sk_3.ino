int potPin = 1; // Potentiometer output connected to analog pin 3
int potVal = 0; // Variable to store the input from the potentiometer


void setup() 
{
Serial.begin(9600);
}

void loop()
{

potVal = analogRead(potPin);   // read the potentiometer value at the input pin
Serial.println(potVal);

if(Serial.available()){
  
int i = 0;
    int brightness = 0;
    while( i < 3){

      int value = (int) (Serial.read() - '0');
      
      if(value >= 0) {
        brightness = brightness * 10 + value;
        i++;
      }
      
    }
    
    analogWrite(9, brightness);

//wait 100 milliseconds so we don't drive ourselves crazy
delay(100);
}
}

