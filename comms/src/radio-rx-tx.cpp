// Feather RFM69 RX/TX Test

#include <Arduino.h>
#include <SPI.h>
#include <RH_RF69.h>
#include <RHReliableDatagram.h>
#include <RingBuf.h>
#include "packet.h"
#include "util.h"

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

// Inbound packet from serial. We build packets one byte at a time since serial has no
// notion of framing, e.g. when a packet ends/begin.
RingBuf<u8, sizeof(Packet)> packet_rx;

// Class to manage message delivery and receipt, using the driver declared above
// RHReliableDatagram rf69_manager(rf69, MY_ADDRESS);

void setup()
{
    Serial.begin(115200);
    // while (!Serial) delay(1); // Wait for Serial Console (comment out line if no computer)

    pinMode(LED, OUTPUT);
    pinMode(RFM69_RST, OUTPUT);
    digitalWrite(RFM69_RST, LOW);

    Serial.println("Kai Kart Radio Initializing!");
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

void loop()
{
    // needs a delay to have time to recieve packets
    delay(25);

    // If there is a packet available, read it and send it over serial
    if (rf69.available())
    {
        digitalWrite(LED, HIGH);

        // Should be a message for us now
        uint8_t buf[RH_RF69_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);
        if (rf69.recv(buf, &len))
        {
            if (!len)
                return;
            buf[len] = 0;
            // Send data over serial to Pi
            Serial.write(buf, len);
        }
        else { Serial.println("Receive failed"); }
    }

    // If there is a packet available from serial, send it over the radio

    if (!Serial.available()) {
        return;
    }

    // Shift bytes in until the beginning is a valid 0xDEADBEEF magic
    packet_rx.pushOverwrite(Serial.read());
    if (!check_magic(packet_rx)) {
        return;
    }

    // We got a valid packet! (hopefully)
    Packet packet;
    for (usize i = 0; i < sizeof(Packet); i++) {
        packet_rx.pop(((u8 *)&packet)[i]);
    }

    // Sanity check
    if (packet.id != PACKET_START_MAGIC) {
        Serial.println("FUCKKKKKK");
        return;
    }

    // Send it over the radio
    rf69.send((uint8_t*) &packet, sizeof(packet));
    rf69.waitPacketSent();
}