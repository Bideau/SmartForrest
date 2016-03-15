#include <LowPower.h>

const int LED=4;

void setup() {
  // put your setup code here, to run once:

  pinMode(LED, OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
  digitalWrite(LED, LOW);
  
  delay(500);
  
  digitalWrite(LED, HIGH);
  // Sleep for 8 s with ADC module and BOD module off
  LowPower.powerDown(SLEEP_4S, ADC_OFF, BOD_OFF);
  
}
