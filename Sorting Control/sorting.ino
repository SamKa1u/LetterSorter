#include <Servo.h>

// initialize servos
Servo bottomServo;
Servo upperServo;

// servo params
const int bottomNeutral = 5;
const int upperNeutral  = 95;
const int tiltAngle     = 25;

// FC-51 IR output pin (LOW = detected)
const int irPin = 7;  

// communication variables
bool first = true;     // ir trigger flag
bool dropped;          // letter removed flag
String cmd = "";



void setup() {
  Serial.begin(9600);     // UART link to Master Controller

  bottomServo.attach(8);
  upperServo.attach(9);

  pinMode(irPin, INPUT);
  delay(500);  

  bottomServo.write(bottomNeutral);
  upperServo.write(upperNeutral);

  Serial.println("Waiting for IR detection...");
  Serial.println("=== IR + UART Letter Sorter ===");
}


void performDrop(int bottomTarget, int upperTarget) {
  bottomServo.write(bottomTarget);
  delay(500);

  upperServo.write(upperTarget);
  delay(2000);

  bottomServo.write(bottomNeutral);
  upperServo.write(upperNeutral);

  Serial.println("Drop complete; servos returned to neutral.\n");
}


void handleRegion(int region) {
  switch (region) {
    case 0:
      Serial.println("→ South detected");
      performDrop(90, upperNeutral + tiltAngle);
      break;

    case 1:
      Serial.println("→ North detected");
      performDrop(10, upperNeutral + tiltAngle);
      break;

    case 2:
      Serial.println("→ West detected");
      performDrop(90, upperNeutral - tiltAngle);
      break;

    case 3:
      Serial.println("→ Midwest detected");
      performDrop(10, upperNeutral - tiltAngle);
      break;

    default:
      Serial.println("→ Unknown region code!");
      break;
  }
  dropped = true;
  Serial.print(dropped);
}


void loop() {
  int irState = digitalRead(irPin);
  // ---- 1. Letter detected ----
  if (irState == LOW) {
    if (first == true) {
      Serial.println("IR_DETECTED");
      first = false;
      dropped = false;
    }
    // ---- 2. Receive region from Raspberry Pi ----
    if (Serial.available()) {
      cmd = Serial.readStringUntil('\n');
      cmd.trim();
      // Serial.print("Message From Pi: ");
      Serial.println(cmd);
    }
    // Expect: REGION:1, REGION:2, REGION:3, or REGION:4
    if (cmd.startsWith("REGION:")) {
      int region = cmd.substring(7).toInt();
      handleRegion(region);
      cmd = "";
    }
    // reset first to rearm IR and clear region
    if (dropped) {
      first = true;

    }
  }
  else {
    first = true;
    cmd = "";
  }
}