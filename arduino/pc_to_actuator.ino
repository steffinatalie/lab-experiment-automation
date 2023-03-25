
int pin1 = 8;
int pin2 = 9;

int ena = 10;

void setup() {
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(ena, OUTPUT);
  
  // Begin serial communication at a baudrate of 9600:
  Serial.begin(9600);
  Serial.setTimeout(1);
}

void loop() {
  while(!Serial.available());

  char r = Serial.read();
  if (r == '1'){
    Serial.print("moving forward\n");
    analogWrite(ena, 255);
    digitalWrite(pin1, HIGH);
    digitalWrite(pin2, LOW);
    delay(35000);
  }
  else if (r == '2'){
    Serial.print("idle\n");
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, LOW);
    delay(2000);
  }
  else if (r == '3'){
    Serial.print("moving backward\n");
    analogWrite(ena, 255);
    digitalWrite(pin1, LOW);
    digitalWrite(pin2, HIGH);
    delay(35000);
  }
}