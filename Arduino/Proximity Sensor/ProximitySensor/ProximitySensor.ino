#include <HCSR04.h>

HCSR04 mySensor(4,3);

void setup() {
  Serial.begin(9600);
}

void loop()
{
  // Make a measure
  mySensor.measure();

  // Print the distance
  Serial.print(mySensor.getInches());
  Serial.print("in, ");
  Serial.print(mySensor.getCm());
  Serial.print("cm");
  Serial.println();

  delay(250);
}
