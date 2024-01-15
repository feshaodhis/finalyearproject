#include <SoftwareSerial.h>

// Serial Object to Arduino GSM
SoftwareSerial SerialGSM(11, 12); // RX, TX

// Variable to hold the data
String powerData = "";

void setup() {
    Serial.begin(115200);
    Serial.println("Setting up!");

    SerialGSM.begin(115200);
    while(!SerialGSM) ;
    SerialGSM.println("Hello, world?");
    if(SerialGSM) {
        Serial.println("Serial GSM Set up");
    }
    else {
        Serial.println("Failed to set up!");
    }
}

void loop() {
    String cmd = "";

    while(SerialGSM.available() > 0) {
        cmd = SerialGSM.readStringUntil('\n');
    }

    if( cmd!= "" ) {
        Serial.print("-> ");
        Serial.println(cmd);
        SerialGSM.println("Got the data");
        powerData = cmd;
    }
}