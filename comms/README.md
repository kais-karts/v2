# Comms
## Description
This is wireless communications between the Go-Karts (each other), and a set of intermediate "nodes" that relay packets (since the track is large). It works using the `ESP-NOW` protocol, and interfaces over serial; writing bytes over serial will send those over the network, and the ESP responds with any packet it receives. So, as far as "communications" goes, there's no distinction between go-karts, nodes, the "server", etc...

The format for packets is defined in `include/packet.h`.

This sub-folder also has the Python side of parsing packets.

## Parameters
**IMPORTANT, THESE MUST MATCH ACROSS SUB-SYSTEMS**
- Baud-rate: `230400`
- Packets format: `include/packet.h`
- Packets framing magic (over serial): `0xDEADBEEF`

## Installation
Get the PlatformIO extension on Visual Studio Code.