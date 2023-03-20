
int pin1 = 8;
int pin2 = 9;

int maju = 5;
int diam = 3;
int mundur = 4;

int ena = 10;

void setup() {
  pinMode(maju, OUTPUT);
  pinMode(diam, OUTPUT);
  pinMode(mundur, OUTPUT);
  
  pinMode(pin1, OUTPUT);
  pinMode(pin2, OUTPUT);
  pinMode(ena, OUTPUT);
  
  // Begin serial communication at a baudrate of 9600:
  Serial.begin(9600);
  Serial.setTimeout(1);
}

void forward(){
  digitalWrite(maju, HIGH);
  digitalWrite(diam, LOW);
  digitalWrite(mundur, LOW);
  
  analogWrite(ena, 255);
  digitalWrite(pin1, HIGH);
  digitalWrite(pin2, LOW);
}

void idle(){
  digitalWrite(maju, LOW);
  digitalWrite(diam, HIGH);
  digitalWrite(mundur, LOW);
  
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, LOW);
}

void backward(){
  digitalWrite(maju, LOW);
  digitalWrite(diam, LOW);
  digitalWrite(mundur, HIGH);
  
  analogWrite(ena, 255);
  digitalWrite(pin1, LOW);
  digitalWrite(pin2, HIGH);
}

void loop() {
  while(!Serial.available());

  char r = Serial.read();
  while (r == '2'){
    Serial.print("forward");
    forward();
    delay(4000);
    r = Serial.read();
  }
  while (r == '3'){
    Serial.print("idle");
    idle();
    delay(4000);
    r = Serial.read();
  }
  while (r == '4'){
    Serial.print("backward");
    backward();
    delay(4000);
    r = Serial.read();
  }
}