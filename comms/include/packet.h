#pragma once

#include <stdint.h>

const uint32_t PACKET_START_MAGIC = 0xDEADBEEF;

enum PacketTag : uint32_t {
    PacketTag_Ping     = 0,
    PacketTag_Location = 1,
    PacketTag_Attack   = 2,
};

typedef struct __attribute__((packed)) {
    uint32_t id;     // Packet ID or magic. If 0xDEADBEEF, it marks start of packet on serial.
    uint32_t tag;    // PacketTag

    union {
        struct {
            uint32_t from;
            uint32_t data;
        } ping;

        struct {
            uint32_t kart_id;
            int32_t x;
            int32_t y;
        } location;

        struct {
            uint32_t kart_id;
            uint32_t item_id;
        } attack;
    } body;

} Packet;

// The sizes of the packets, could be used for framing
#define PACKET_SIZE_PING sizeof(Packet)
#define PACKET_SIZE_LOCATION sizeof(Packet)
#define PACKET_SIZE_ATTACK sizeof(Packet)

// Check if the first 4 bytes of a ring buffer match the magic
template <typename RingBufT>
static bool check_magic(RingBufT& buf) {
    const uint8_t BYTES[4] = {
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
