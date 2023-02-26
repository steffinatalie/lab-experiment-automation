char x;

void setup(){
  Serial.begin(9600);
  Serial.setTimeout(1);
}
void loop(){
  while(!Serial.available());
  x = Serial.read();
  if (x == 'r'){
    Serial.print("reading");
  }
  else{
    Serial.print("not reading");
  }
}