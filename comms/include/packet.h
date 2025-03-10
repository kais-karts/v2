#pragma once

#include "util.h"

const u32 PACKET_START_MAGIC = 0xDEADBEEF;

typedef struct __attribute__((packed)) {
    u32 id;     // Random identifier of this packet, to avoid infinite echoing in the network
                // NOTE: When the Raspberry Pi and ESP32 talk over serial, this should be 0xDEADBEEF.
                //       This is used for framing, i.e. knowing when packets begin on the serial steam.
    
    enum {
        Ping,
    } tag;
    union {
        // Ping :: Used to test the network (example packet)
        struct {
            u32 from;   // Go-Kart ID (0-7)
            u32 data;
        } ping;
    } body;
} Packet;

static bool check_magic(RingBuf<u8, sizeof(Packet)>& buf) {
    // 0xDEADBEEF (little endian bruh)
    const u8 BYTES[4] = {
        (PACKET_START_MAGIC) & 0xFF,
        (PACKET_START_MAGIC >> 8) & 0xFF,
        (PACKET_START_MAGIC >> 16) & 0xFF,
        (PACKET_START_MAGIC >> 24) & 0xFF,
    };
    return (buf[0] == BYTES[0])
        && (buf[1] == BYTES[1])
        && (buf[2] == BYTES[2])
        && (buf[3] == BYTES[3]);
}