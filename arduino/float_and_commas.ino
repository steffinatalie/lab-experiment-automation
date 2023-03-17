float a = 100, b = 7;

void setup() {
  // Begin serial communication at a baudrate of 9600:
  Serial.begin(9600);
}

void loop() {
  Serial.print(a);
//  Serial.print(", ");
//  Serial.print(b);
  Serial.print('\n');

  delay(1000);
}