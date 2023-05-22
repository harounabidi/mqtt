#include <Servo.h> 

Servo lockServo;

int lockPos = 15;               // Locked position limit
int unlockPos = 75;             // Unlocked position limit

boolean locked = true;

int redLEDPin = 5;
int greenLEDPin = 6;

void setup() {
  Serial.begin(9600); 
  lockServo.attach(3);
  lockServo.write(lockPos); 
  pinMode(redLEDPin, OUTPUT);     // LED startup sequence
  pinMode(greenLEDPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {

    String message = Serial.readString();
    
    if(message == "Access Granted") {

      Serial.write("Access Granted");

      digitalWrite(greenLEDPin, HIGH);    // Green LED sequence
      delay(200);
      digitalWrite(greenLEDPin, LOW);
      delay(200);
      digitalWrite(greenLEDPin, HIGH);
      delay(200);
      digitalWrite(greenLEDPin, LOW);
      delay(200);

      // If the lock is closed then open it
      if (locked == true) {
        lockServo.write(unlockPos);
        locked = false;
      }
      // If the lock is open then close it
      else if (locked == false) {
        lockServo.write(lockPos);
        locked = true;
      }
    } 
    else {
      Serial.write("Access Denied");

      digitalWrite(redLEDPin, HIGH);      // Red LED sequence
      delay(200);
      digitalWrite(redLEDPin, LOW);
      delay(200);
      digitalWrite(redLEDPin, HIGH);
      delay(200);
      digitalWrite(redLEDPin, LOW);
      delay(200);
    }
  }
}
