const int xPin = A0;
const int yPin = A1;
const int zPin = A2;

void setup() {
  Serial.begin(115200);
}

void loop() {
  int xValue = analogRead(xPin);
  int yValue = analogRead(yPin);
  int zValue = analogRead(zPin);

  float xAccel = ((float)xValue - 330) / 65;  // ADXL335 @ 3.3V: 330 = 1.65/3.3*1023, 65 = 0.33/3.3*1023
  float yAccel = ((float)yValue - 330) / 65;
  float zAccel = ((float)zValue - 330) / 65;

  // Serial.print("X : ");
  Serial.print(xAccel);
  // Serial.print("\t");
  Serial.print(",");
  // Serial.print("Y : ");
  Serial.print(yAccel);
  // Serial.print("\t");
  Serial.print(",");
  // Serial.print("Z : ");
  Serial.print(zAccel);
  Serial.println();

  delay(20);
}
