#include <BluetoothSerial.h>
#include <HardwareSerial.h>

#define UART_RX 16
#define UART_TX 17

////////////////////////////////////////////////////////////////////
// BLUETOOTH SET UP
////////////////////////////////////////////////////////////////////
BluetoothSerial SerialBT;

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

// Hardware Serial
HardwareSerial Serial2Arduino(2);

/////////////////////////////////////////////////////////////

void setup()
{
    ///////////////////////////////////////////////
    // Setup Serial
    ///////////////////////////////////////////////
    Serial.begin(115200);
    Serial.println("Serial UP & Running!");
    Serial.println("");

    // Hardware Serial Setup for Arduino Communication
    Serial2Arduino.begin(9600, SERIAL_8N1, UART_RX, UART_TX);

    ////////////////////////////////////////
    // Start Bluetooth
    ////////////////////////////////////////
    SerialBT.begin("Power Device"); // Bluetooth device name
    Serial.println("Bluetooth UP & RUNNING");

    Serial.println("Setup complete");
}

void loop()
{
    Serial.println("");

    String data = "";

    while (Serial2Arduino.available() > 0)
    {
        char c = Serial2Arduino.read();
        Serial.print(c);

        data += c;

        if (c == '\n')
        {
            // New line character to show end of message block

            if (data.length() > 3)
            {
                sendToBT(data);
            }

            data = "";
        }
    }
}

void sendToBT(String msg)
{
    Serial.print("Sendnding -> ");
    Serial.print(msg);

    char buf[msg.length() + 1];
    msg.toCharArray(buf, msg.length() + 1);

    for (int i = 0; i < msg.length(); i++)
    {
        SerialBT.write((uint8_t)buf[i]);
    }
}