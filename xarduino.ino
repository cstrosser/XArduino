/*
PI_XArduino

Interfaces with XArduino for PythonInterface (X-Plane 10)

Copyright (c) 2012 by Chris Strosser
*/

void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  pinMode(10, INPUT);
  pinMode(11, INPUT);
  pinMode(12, INPUT);
  pinMode(13, INPUT);
}

void loop() {
  int sensorValue2 = digitalRead(2);
  int sensorValue3 = digitalRead(3);
  int sensorValue4 = digitalRead(4);
  int sensorValue5 = digitalRead(5);
  int sensorValue6 = digitalRead(6);
  int sensorValue7 = digitalRead(7);
  int sensorValue8 = digitalRead(8);
  int sensorValue9 = digitalRead(9);
  int sensorValue10 = digitalRead(10);
  int sensorValue11 = digitalRead(11);
  int sensorValue12 = digitalRead(12);
  int sensorValue13 = digitalRead(13);
  
  Serial.print('H');
  Serial.print(",");
  Serial.print(sensorValue2, DEC);
  Serial.print(",");
  Serial.print(sensorValue3, DEC);
  Serial.print(",");
  Serial.print(sensorValue11, DEC);
  Serial.print(",");
  Serial.print(sensorValue12, DEC);
  Serial.print(",");
  Serial.print(sensorValue8, DEC);
  Serial.print(",");
  Serial.print(sensorValue9, DEC);
  Serial.print(",");
  Serial.print(sensorValue10, DEC);
  Serial.print(",");
  Serial.print(sensorValue13, DEC);
  Serial.print(",");
  Serial.print(sensorValue7, DEC);
  Serial.print(",");
  Serial.print(sensorValue6, DEC);
  Serial.print(",");
  Serial.print(sensorValue5, DEC);
  Serial.print(",");
  Serial.print(sensorValue4, DEC);
  //Serial.print(",");
  Serial.println();
  delay(100);
}



