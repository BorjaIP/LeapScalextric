void setup() {
  // SETUP: Open serial at 9600bps
  Serial.begin(9600);
  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }  
}

void loop() {
  /*LOOP:
  /     1 - Read from Serial
  /     2 - Tune PWM
  */
    
  if(Serial.available() > 0) {
    String inString = Serial.readStringUntil(';');
    int inTrack = inString.toInt();
    Serial.print(inTrack);
    Serial.print(" ");
    
    inString = Serial.readStringUntil(';');
    int inPwm = inString.toInt();
    Serial.println(inPwm);

    if(inPwm<100) 
      analogWrite(inTrack, 0);
    else if (inPwm>255)
      analogWrite(inTrack, 255);
    else
      analogWrite(inTrack, inPwm);
      
    Serial.println("<Arduino is ready>");
  }
}

