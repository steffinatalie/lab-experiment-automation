float a = 100, b = 7, c = 10, d=1234;

void setup() {
  // Begin serial communication at a baudrate of 9600:
  Serial.begin(9600);
}

void loop() {
  Serial.print(a);
  Serial.print(", ");
  Serial.print(b);
  Serial.print(", ");
  Serial.print(c);
  Serial.print(", ");
  Serial.print(d);
  Serial.print('\n');
  

  delay(1000);
}