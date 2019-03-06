//Pines de lectura del encoder
int encoderA = 7;
int encoderB = 3;

// Valores del encoders
volatile int valorA = 0;
volatile int valorB = 0;

void encoder(){
  valorA = digitalRead(encoderA);
  valorB = digitalRead(encoderB);
  Serial.println(valorA);
  Serial.println(valorB);
}

void setup() {
  Serial.begin(9600);
  
  // Configuramos los pines del encoder como entradas
  pinMode(encoderA, INPUT);
  pinMode(encoderB, INPUT);
  
  // Leemos la posición inicial del encoder
  valorA = digitalRead(encoderA); 
  valorB = digitalRead(encoderB);

  // Interrupciones cuando cambia el valor del encoder
  attachInterrupt(digitalPinToInterrupt(encoderA), encoder, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoderB), encoder, CHANGE);
}

void loop() {

}
