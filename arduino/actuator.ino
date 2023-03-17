//#include <SharpIR.h>
//
//// Define model and input pin:
//#define IRPin A1
//#define model 430

// Create variable to store the distance:
int distance_cm;


// Create a new instance of the SharpIR class:
//SharpIR mySensor = SharpIR(IRPin, model);

int pin1 = 8;
int pin2 = 9;

int ena = 10;

void setup(){
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(ena, OUTPUT);

//  Serial.begin(9600);
}

//void loop(){
//  // Get a distance measurement and store it as distance_cm:
//  distance_cm = mySensor.distance();
//
//  Serial.print(distance_cm);
//  Serial.print('\n');
//
//  delay(1000);
//
//  if (distance_cm 
//}

void loop(){
  analogWrite(ena, 255);
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, LOW);
  delay(35000);

  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
  delay(2000);

  analogWrite(ena, 255);
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, HIGH);
  delay(35000);

  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
  delay(2000);

  
}