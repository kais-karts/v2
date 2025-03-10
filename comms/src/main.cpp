#include <Arduino.h>
#include <WiFi.h>
#include <esp_now.h>
#include <esp_wifi.h>
#include <esp_wifi_types.h>
#include <RingBuf.h>

#include "packet.h"
#include "util.h"

// Packet unique IDs seen recently, to avoid double-echoing
RingBuf<u32, 32> seen;

// Inbound packet from serial. We build packets one byte at a time since serial has no
// notion of framing, e.g. when a packet ends/begin.
RingBuf<u8, sizeof(Packet)> packet_rx;

// Callback when a packet is received from ESP-NOW
void on_recv_packet(const u8* mac, const u8* data, i32 len);
// Send a packet over ESP-NOW
void send_packet(Packet* packet, bool overwrite_id = true);

void setup() {
    WiFi.mode(WIFI_STA);

    // Start ESP-NOW
    if (esp_now_init() != ESP_OK) {
        panic("Error initializing ESP-NOW");
    }

    // Add ff:ff:ff:ff:ff:ff as a peer (i.e. broadcast to all)
    esp_now_peer_info_t peer = {
        .peer_addr = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF},
        .channel = 1,
        .encrypt = false,
    };
    esp_err_t res;
    if ((res = esp_now_add_peer(&peer)) != ESP_OK) {
        panic(esp_err_to_name(res));
    }

    // Register callbacks
    esp_now_register_recv_cb(esp_now_recv_cb_t(on_recv_packet));
}

void loop() {
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
        packet_rx.pop(((u8*)&packet)[i]);
    }

    // Sanity check
    if (packet.id != PACKET_START_MAGIC) {
        Serial.println("FUCKKKKKK");
        return;
    }

    // Send it across the network
    send_packet(&packet);
}

void on_recv_packet(const u8* mac, const u8* data, i32 len) {
    if (len != sizeof(Packet)) {
        Serial.println("Received the wrong payload size!");
        return;
    }

    Packet packet;
    memcpy(&packet, data, sizeof(Packet));

    for (usize i = 0; i < seen.size(); i++) {
        if (seen[i] == packet.id) {
            // Packet has already been through this node, so skip it
            return;
        }
    }

    // Send packet on serial
    u32 packet_id = packet.id;
    packet.id = PACKET_START_MAGIC;

    Serial.write((u8*)&packet, sizeof(packet));

    packet.id = packet_id;

    // Echo packet
    send_packet(&packet, false);
}

void send_packet(Packet* packet, bool overwrite_id) {
    if (overwrite_id) {
        packet->id = random();
    }
    seen.pushOverwrite(packet->id);

    u8 addr[6] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};
    
    esp_now_send(addr, (u8*) packet, sizeof(Packet));
}