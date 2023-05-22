#include <SPI.h> 
#include <RFID.h>

RFID rfid(10, 9);                               // D10:pin of tag reader SDA. D9:pin of tag reader RST 
unsigned char status; 
unsigned char str[MAX_LEN];                     // MAX_LEN is 16: size of the array 

String accessGranted [2] = {"73275363"};        // RFID serial numbers to grant access to
int accessGrantedSize = 2;                      // The number of serial numbers

int redLEDPin = 5;
int greenLEDPin = 6;

void setup() { 
  Serial.begin(9600);     // Serial monitor is only required to get tag ID numbers and for troubleshooting
  SPI.begin();            // Start SPI communication with reader
  rfid.init();            // initialization 
  pinMode(redLEDPin, OUTPUT);     // LED startup sequence
  pinMode(greenLEDPin, OUTPUT);
} 

void loop() { 
  // Wait for a tag to be placed near the reader
  if (rfid.findCard(PICC_REQIDL, str) == MI_OK) { 
    String temp = "";         // Temporary variable to store the read RFID number
    // Anti-collision detection, read tag serial number
    if (rfid.anticoll(str) == MI_OK) { 
      // Record the tag serial number 
      for (int i = 0; i < 4; i++) { 
        temp = temp + (0x0F & (str[i] >> 4)); 
        temp = temp + (0x0F & str[i]); 
      } 
      checkAccess (temp);     // Check if the identified tag is an allowed to open tag
    } 
    rfid.selectTag(str);      // Lock card to prevent a redundant read, removing the line will make the sketch read cards continually
  }
  rfid.halt();
}

// Function to check if an identified tag is registered to allow access
void checkAccess (String temp) {
  boolean granted = false;
  // Runs through all tag ID numbers registered in the array
  for (int i=0; i <= (accessGrantedSize-1); i++) {
    if(accessGranted[i] == temp) {
      granted = true;
      Serial.println ("Access Granted");
      digitalWrite(greenLEDPin, HIGH);    // Green LED sequence
      delay(200);
      digitalWrite(greenLEDPin, LOW);
      delay(200);
      digitalWrite(greenLEDPin, HIGH);
      delay(200);
      digitalWrite(greenLEDPin, LOW);
      delay(200);
    }
  }
  // If the tag is not found
  if (granted == false) {
    Serial.println ("Access Denied");
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