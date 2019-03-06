int pirPin = D4;

void setup() {
  Serial.begin(9600);
  pinMode(pirPin, INPUT_PULLUP);
}

void loop() {
  int pirVal = digitalRead(pirPin);

    Serial.println(pirVal);
  
}
