int LED = 13; // define PIN for LED - Biultin LED is on PIN 13
int PIR = 2;  // define PIN for PIR motion sensor - PIN D2

void setup() {
  pinMode(LED,OUTPUT); // define LED pin as output
  pinMode(PIR,INPUT);  // define PIR pin as input
}

void loop() {
  digitalWrite(LED,digitalRead(PIR)); // Write value of PIR sensor to LED
}
