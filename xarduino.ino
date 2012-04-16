/*
PI_XArduino

Interfaces with XArduino for PythonInterface (X-Plane 10)

Copyright (c) 2012 by Chris Strosser
*/

#define BUTTON1 36
#define BUTTON2 37
#define BUTTON3 38
#define BUTTON4 39
#define SWITCH1 40
#define SWITCH2 41
#define SWITCH3 42
#define SWITCH4 43
#define SWITCH5_A 45
#define SWITCH5_B 44
#define SWITCH6_A 47
#define SWITCH6_B 46
#define SWITCH7 48
#define SWITCH8 49
#define SWITCH9 50
#define SWITCH10 51
#define SWITCH11 52
#define SWITCH12 53
#define LED_SWITCH5 5
#define LED_SWITCH6 4
#define LED_SWITCH7 3
#define LED_SWITCH8 2
#define LED_SWITCH9 9
#define LED_SWITCH10 8
#define LED_SWITCH11 7
#define LED_SWITCH12 6

void setup() {
  Serial.begin(9600);
  
  pinMode(BUTTON1, INPUT);
  pinMode(BUTTON2, INPUT);
  pinMode(BUTTON3, INPUT);
  pinMode(BUTTON4, INPUT);
  pinMode(SWITCH1, INPUT);
  pinMode(SWITCH2, INPUT);
  pinMode(SWITCH3, INPUT);
  pinMode(SWITCH4, INPUT);
  pinMode(SWITCH5_A, INPUT);
  pinMode(SWITCH5_B, INPUT);
  pinMode(SWITCH6_A, INPUT);
  pinMode(SWITCH6_B, INPUT);
  pinMode(SWITCH7, INPUT);
  pinMode(SWITCH8, INPUT);
  pinMode(SWITCH9, INPUT);
  pinMode(SWITCH10, INPUT);
  pinMode(SWITCH11, INPUT);
  pinMode(SWITCH12, INPUT);
  
  pinMode(LED_SWITCH5, OUTPUT);
  pinMode(LED_SWITCH6, OUTPUT);
  pinMode(LED_SWITCH7, OUTPUT);
  pinMode(LED_SWITCH8, OUTPUT);
  pinMode(LED_SWITCH9, OUTPUT);
  pinMode(LED_SWITCH10, OUTPUT);
  pinMode(LED_SWITCH11, OUTPUT);
  pinMode(LED_SWITCH12, OUTPUT);
}

void loop() {
  int sensorButton1 = digitalRead(BUTTON1);
  int sensorButton2 = digitalRead(BUTTON2);
  int sensorButton3 = digitalRead(BUTTON3);
  int sensorButton4 = digitalRead(BUTTON4);
  int sensorSwitch1 = digitalRead(SWITCH1);
  int sensorSwitch2 = digitalRead(SWITCH2);
  int sensorSwitch3 = digitalRead(SWITCH3);
  int sensorSwitch4 = digitalRead(SWITCH4);
  int sensorSwitch5 = 1;
  int sensorSwitch5A = digitalRead(SWITCH5_A);
  int sensorSwitch5B = digitalRead(SWITCH5_B);
  int sensorSwitch6 = 1;
  int sensorSwitch6A = digitalRead(SWITCH6_A);
  int sensorSwitch6B = digitalRead(SWITCH6_B);
  int sensorSwitch7 = digitalRead(SWITCH7);
  int sensorSwitch8 = digitalRead(SWITCH8);
  int sensorSwitch9 = digitalRead(SWITCH9);
  int sensorSwitch10 = digitalRead(SWITCH10);
  int sensorSwitch11 = digitalRead(SWITCH11);
  int sensorSwitch12 = digitalRead(SWITCH12);
  
  if (sensorSwitch5A) {
    sensorSwitch5 = 2;
  } else if (sensorSwitch5B) {
    sensorSwitch5 = 0;
  }
  if (sensorSwitch6A) {
    sensorSwitch6 = 2;
  } else if (sensorSwitch6B) {
    sensorSwitch6 = 0;
  }
  
  Serial.print('H');
  Serial.print(",");
  Serial.print(sensorButton1, DEC);
  Serial.print(",");
  Serial.print(sensorButton2, DEC);
  Serial.print(",");
  Serial.print(sensorButton3, DEC);
  Serial.print(",");
  Serial.print(sensorButton4, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch1, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch2, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch3, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch4, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch5, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch6, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch7, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch8, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch9, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch10, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch11, DEC);
  Serial.print(",");
  Serial.print(sensorSwitch12, DEC);
  //Serial.print(",");
  Serial.println();
  
  int ledOff = 0;
  int ledOn = 60;
  if (sensorSwitch5 == 1) {
    analogWrite(LED_SWITCH5, ledOn / 2);
  } else if (sensorSwitch5 == 2) {
    analogWrite(LED_SWITCH5, ledOn);
  } else {
    analogWrite(LED_SWITCH5, ledOff);
  }
  if (sensorSwitch6 == 1) {
    analogWrite(LED_SWITCH6, ledOn / 2);
  } else if (sensorSwitch6 == 2) {
    analogWrite(LED_SWITCH6, ledOn);
  } else {
    analogWrite(LED_SWITCH6, ledOff);
  }
  analogWrite(LED_SWITCH7, sensorSwitch7 ? ledOn : ledOff);
  analogWrite(LED_SWITCH8, sensorSwitch8 ? ledOn : ledOff);
  analogWrite(LED_SWITCH9, sensorSwitch9 ? ledOn : ledOff);
  analogWrite(LED_SWITCH10, sensorSwitch10 ? ledOn : ledOff);
  analogWrite(LED_SWITCH11, sensorSwitch11 ? ledOn : ledOff);
  analogWrite(LED_SWITCH12, sensorSwitch12 ? ledOn : ledOff);
  
  delay(50);
}