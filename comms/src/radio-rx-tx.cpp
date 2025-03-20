// Feather RFM69 RX/TX Test

#include <Arduino.h>
#include <SPI.h>
#include <RH_RF69.h>
#include <RHReliableDatagram.h>

/************ Radio Setup ***************/
#define MY_ADDRESS 1

// Change to 434.0 or other frequency, must match RX's freq!
#define RF69_FREQ 915.0

#define RFM69_CS 8
#define RFM69_INT 7
#define RFM69_RST 4
#define LED 13

// Singleton instance of the radio driver
RH_RF69 rf69(RFM69_CS, RFM69_INT);

// Class to manage message delivery and receipt, using the driver declared above
// RHReliableDatagram rf69_manager(rf69, MY_ADDRESS);

void setup()
{
    Serial.begin(115200);
    // while (!Serial) delay(1); // Wait for Serial Console (comment out line if no computer)

    pinMode(LED, OUTPUT);
    pinMode(RFM69_RST, OUTPUT);
    digitalWrite(RFM69_RST, LOW);

    Serial.println("Feather RFM69 RX Test!");
    Serial.println();

    // manual reset
    digitalWrite(RFM69_RST, HIGH);
    delay(10);
    digitalWrite(RFM69_RST, LOW);
    delay(10);

    if (!rf69.init())
    {
        Serial.println("RFM69 radio init failed");
        while (1)
            ;
    }
    Serial.println("RFM69 radio init OK!");

    // Defaults after init are 434.0MHz, modulation GFSK_Rb250Fd250, +13dbM (for low power module)
    // No encryption
    if (!rf69.setFrequency(RF69_FREQ))
    {
        Serial.println("setFrequency failed");
    }

    // If you are using a high power RF69 eg RFM69HW, you *must* set a Tx power with the
    // ishighpowermodule flag set like this:
    rf69.setTxPower(20, true); // range from 14-20 for power, 2nd arg must be true for 69HCW

    // The encryption key has to be the same as the one in the server
    uint8_t key[] = {0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08,
                     0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08};
    rf69.setEncryptionKey(key);

    Serial.print("RFM69 radio @");
    Serial.print((int)RF69_FREQ);
    Serial.println(" MHz");
}

uint8_t counter = 0;
uint8_t others_counter = 0;
uint8_t missed_packets = 0;

void loop()
{
    // needs a delay to have time to recieve packets
    delay(25);
    char radiopacket[20] = "Radio 1 says #";
    itoa(counter++, radiopacket + 14, 10);
    Serial.print("Radio 1 sending ");
    Serial.println(counter);

    // Send a message!
    rf69.send((uint8_t *)radiopacket, strlen(radiopacket));
    rf69.waitPacketSent();
    Serial.println("Sent");

    if (rf69.available())
    {
        digitalWrite(LED, HIGH);
        others_counter++;

        // Should be a message for us now
        uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);
        if (rf69.recv(buf, &len))
        {
            if (!len)
                return;
            buf[len] = 0;
            Serial.print("Received of len ");
            Serial.print(len);
            Serial.print(": ");
            Serial.println((char *)buf);
            Serial.print("RSSI: ");
            Serial.println(rf69.lastRssi(), DEC);
        }
        else
        {
            Serial.println("Receive failed");
        }
        digitalWrite(LED, LOW);
    }
}