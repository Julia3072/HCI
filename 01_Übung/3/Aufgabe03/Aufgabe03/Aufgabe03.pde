import processing.serial.*;

Serial myPort;  // Create object from Serial class
int time = millis();
BufferedReader reader;
String line;

void setup() 
{
  size(200, 200); //make our canvas 200 x 200 pixels big
  String portName = Serial.list()[0]; //change the 0 to a 1 or 2 etc. to match your port
  myPort = new Serial(this, portName, 9600);
  reader = createReader("pulse_parsed.csv");
}

void draw() {

  if (millis() > time) {
    time = millis() + 10;
    try {
      line = reader.readLine();
    } 
    catch (IOException e) {
      e.printStackTrace();
      line = null;
    }

    if (line == null) {
      noLoop();
    } else {

      String[] redPieces = split(line, " ");
      int value = (int(redPieces[1]))/3;
      myPort.write(value);        
      println(value);
    }
  }
}