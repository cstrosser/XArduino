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
#define SWITCH5 48
#define SWITCH6 35
#define SWITCH7 34
#define SWITCH8 33
#define SWITCH9_A 45
#define SWITCH9_B 44
#define SWITCH10_A 47
#define SWITCH10_B 46
#define SWITCH11_A 31
#define SWITCH11_B 32
#define SWITCH12 49
#define SWITCH13 50
#define SWITCH14 51
#define SWITCH15 52
#define SWITCH16 53
#define LED_SWITCH9 5
#define LED_SWITCH10 4
#define LED_SWITCH11 3
#define LED_SWITCH12 2
#define LED_SWITCH13 9
#define LED_SWITCH14 8
#define LED_SWITCH15 7
#define LED_SWITCH16 6

int lastValue[20];
boolean change = true;

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
  pinMode(SWITCH5, INPUT);
  pinMode(SWITCH6, INPUT);
  pinMode(SWITCH7, INPUT);
  pinMode(SWITCH8, INPUT);
  pinMode(SWITCH9_A, INPUT);
  pinMode(SWITCH9_B, INPUT);
  pinMode(SWITCH10_A, INPUT);
  pinMode(SWITCH10_B, INPUT);
  pinMode(SWITCH11_A, INPUT);
  pinMode(SWITCH11_B, INPUT);
  pinMode(SWITCH12, INPUT);
  pinMode(SWITCH13, INPUT);
  pinMode(SWITCH14, INPUT);
  pinMode(SWITCH15, INPUT);
  pinMode(SWITCH16, INPUT);
  
  pinMode(LED_SWITCH9, OUTPUT);
  pinMode(LED_SWITCH10, OUTPUT);
  pinMode(LED_SWITCH11, OUTPUT);
  pinMode(LED_SWITCH12, OUTPUT);
  pinMode(LED_SWITCH13, OUTPUT);
  pinMode(LED_SWITCH14, OUTPUT);
  pinMode(LED_SWITCH15, OUTPUT);
  pinMode(LED_SWITCH16, OUTPUT);
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
  int sensorSwitch5 = digitalRead(SWITCH5);
  int sensorSwitch6 = digitalRead(SWITCH6);
  int sensorSwitch7 = digitalRead(SWITCH7);
  int sensorSwitch8 = digitalRead(SWITCH8);
  int sensorSwitch9 = 1;
  int sensorSwitch9A = digitalRead(SWITCH9_A);
  int sensorSwitch9B = digitalRead(SWITCH9_B);
  int sensorSwitch10 = 1;
  int sensorSwitch10A = digitalRead(SWITCH10_A);
  int sensorSwitch10B = digitalRead(SWITCH10_B);
  int sensorSwitch11 = 1;
  int sensorSwitch11A = digitalRead(SWITCH11_A);
  int sensorSwitch11B = digitalRead(SWITCH11_B);
  int sensorSwitch12 = digitalRead(SWITCH12);
  int sensorSwitch13 = digitalRead(SWITCH13);
  int sensorSwitch14 = digitalRead(SWITCH14);
  int sensorSwitch15 = digitalRead(SWITCH15);
  int sensorSwitch16 = digitalRead(SWITCH16);
  
  if (sensorSwitch9A) {
    sensorSwitch9 = 2;
  } else if (sensorSwitch9B) {
    sensorSwitch9 = 0;
  }
  if (sensorSwitch10A) {
    sensorSwitch10 = 2;
  } else if (sensorSwitch10B) {
    sensorSwitch10 = 0;
  }
  if (sensorSwitch11A) {
    sensorSwitch11 = 2;
  } else if (sensorSwitch11B) {
    sensorSwitch11 = 0;
  }
  
  unsigned int out = 0;
  out = setBit(out, 0, sensorButton1);
  out = setBit(out, 1, sensorButton2);
  out = setBit(out, 2, sensorButton3);
  out = setBit(out, 3, sensorButton4);
  out = setBit(out, 4, sensorSwitch1);
  out = setBit(out, 5, sensorSwitch2);
  out = setBit(out, 6, sensorSwitch3);
  out = setBit(out, 7, sensorSwitch4);
  out = setBit(out, 8, sensorSwitch5);
  out = setBit(out, 9, sensorSwitch6);
  out = setBit(out, 10, sensorSwitch7);
  out = setBit(out, 11, sensorSwitch8);
  out = setBit(out, 12, sensorSwitch9);
  out = setBit(out, 13, sensorSwitch10);
  out = setBit(out, 14, sensorSwitch11);
  out = setBit(out, 15, sensorSwitch12);
  out = setBit(out, 16, sensorSwitch13);
  out = setBit(out, 17, sensorSwitch14);
  out = setBit(out, 18, sensorSwitch15);
  out = setBit(out, 19, sensorSwitch16);
  
  if (change) {
    Serial.print('H');
    Serial.print(",");
    Serial.print(out);
    Serial.println();
    Serial.print('H');
    Serial.print(",");
    Serial.print(out);
    Serial.println();
    Serial.print('H');
    Serial.print(",");
    Serial.print(out);
    Serial.println();
    change = false;
  }
  
  int ledOff = 0;
  int ledOn = 60;
  if (sensorSwitch9 == 1) {
    analogWrite(LED_SWITCH9, ledOn / 2);
  } else if (sensorSwitch9 == 2) {
    analogWrite(LED_SWITCH9, ledOn);
  } else {
    analogWrite(LED_SWITCH9, ledOff);
  }
  if (sensorSwitch10 == 1) {
    analogWrite(LED_SWITCH10, ledOn / 2);
  } else if (sensorSwitch10 == 2) {
    analogWrite(LED_SWITCH10, ledOn);
  } else {
    analogWrite(LED_SWITCH10, ledOff);
  }
  if (sensorSwitch11 == 1) {
    analogWrite(LED_SWITCH11, ledOn / 2);
  } else if (sensorSwitch11 == 2) {
    analogWrite(LED_SWITCH11, ledOn);
  } else {
    analogWrite(LED_SWITCH11, ledOff);
  }
  analogWrite(LED_SWITCH12, sensorSwitch12 ? ledOn : ledOff);
  analogWrite(LED_SWITCH13, sensorSwitch13 ? ledOn : ledOff);
  analogWrite(LED_SWITCH14, sensorSwitch14 ? ledOn : ledOff);
  analogWrite(LED_SWITCH15, sensorSwitch15 ? ledOn : ledOff);
  analogWrite(LED_SWITCH16, sensorSwitch16 ? ledOn : ledOff);
}

int setBit(unsigned int value, int bitNumber, int state)
{
  if (lastValue[bitNumber] != state) {
    change = true;
    lastValue[bitNumber] = state;
  }
  
  if (state == 0) {
    value &= ~(1 << bitNumber);
  } else {
    value |= (state << bitNumber);
  }
  return value;
}
