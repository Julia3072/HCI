//Konstanten
int startUntenX = 250;
int startUntenY = 400;
  
int startObenX = 250;
int startObenY = 125;

BufferedReader reader;
String line;

void setup() {
  size(500, 500);
  
  //Datei einlesen
  reader = createReader("pulse_parsed.csv");
}

int time = millis();

void draw() {
  if(millis() > time) {
    time = millis() + 10;
    
    clear();
    fill(150, 150, 150);
    rect(-1, -1, 501, 501);
  
    try {
      line = reader.readLine();
    } catch(IOException e) {
      e.printStackTrace();
      line = null;
    }
    
    if(line == null) {
     noLoop(); 
    } else {
      String[] pieces = split(line, " ");
      int value = int(pieces[1]) / 5;
      
      //Herz zeichnen
      int linksX = 50 - value;
      int linksY = 50 - value;
      
      int rechtsX = 450 + value;
      int rechtsY = 50 - value;
      
      stroke(139,0,0);
      fill(255,0,0);
      bezier(startObenX, startObenY + (value / 5), linksX, linksY, linksX, linksY, startUntenX, startUntenY);
      bezier(startObenX, startObenY + (value / 5), rechtsX, rechtsY, rechtsX, rechtsY, startUntenX, startUntenY);
    }
  }
}