#include <Servo.h>


void handleOn(Servo &upper);
void handleOff(Servo &lower);
void sweepTo(Servo &type, int from, int to, int stepDelay);

Servo servoUpper;
Servo servoLower;

const int UPPER_PIN = 9;
const int LOWER_PIN = 10;

const int UPPER_START = 90;
const int LOWER_START = 90;

void setup() {
  Serial.begin(9600);
  servoUpper.attach(UPPER_PIN);
  servoLower.attach(LOWER_PIN);

  // Move both servos to starting position
  servoUpper.write(UPPER_START);
  servoLower.write(LOWER_START);
  delay(500);

  Serial.println("Ready. Type 'on' or 'off':");
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input == "on") {
      Serial.println("ON  → Lower servo: anticlockwise 90°");
      switchOn(servoLower);
    }
    else if (input == "off") {
      Serial.println("OFF → Upper servo: clockwise 90°");
      switchOff(servoUpper);
    }
    else {
      Serial.println("Unknown command. Type 'on' or 'off'.");
    }
  }
}

// Lower servo: anticlockwise 90° then return 
void switchOn(Servo &lower) {
  int target = LOWER_START + 90;        // anticlockwise = increasing angle
  sweepTo(lower, LOWER_START, target, 10);
  delay(300);
  sweepTo(lower, target, LOWER_START, 10);
  Serial.println("Lower servo returned to start.");
}

// Upper servo: clockwise 90° then return ---
void switchOff(Servo &upper) {
  int target = UPPER_START - 90;        // clockwise = decreasing angle
  sweepTo(upper, UPPER_START, target, 10);
  delay(300);
  sweepTo(upper, target, UPPER_START, 10);
  Serial.println("Upper servo returned to start.");
}

// Smooth sweep from one angle to another 
void sweepTo(Servo &type, int from, int to, int stepDelay) {
  if (from < to) {
    for (int angle = from; angle <= to; angle++) {
      type.write(angle);
      delay(stepDelay);
    }
  } else {
    for (int angle = from; angle >= to; angle--) {
      type.write(angle);
      delay(stepDelay);
    }
  }
}
