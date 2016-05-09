import processing.serial.*;

String val;     // Data received from the serial port
PrintWriter output;

// I know that the first port in the serial list on my mac
// is Serial.list()[0].
// On Windows machines, this generally opens COM1.
// Open whatever port is the one you're using.

String portName = Serial.list()[1]; //change the 0 to a 1 or 2 etc. to match your port
Serial myPort = new Serial(this, portName, 9600); 

void setup(){
    output = createWriter("arduino_out.txt"); 
}

void draw()
{
  output = createWriter("arduino_out.txt"); 

  
  if ( myPort.available() > 0) 
  {  // If data is available,
  val = myPort.readStringUntil('\n');         // read it and store it in val
  }
  
  if (val != "null" && val != null){
    
      
      output.println(val);
      output.flush();  // Writes the remaining data to the file
      output.close();
      println(val); //print it out in the console
  }
}