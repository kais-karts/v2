''' This module is responsible for reading from and sending packets to the queue. '''

from comms import PacketQueue, Packet
from constants import PORT, KART_ID
from actions import update_ranking, apply_item

# Packets that will be sent are location {kart_id}, attack {kart_id, item_id}
# I assume Packet will have a command and data attribute
# Packet.command will be a string with the command (Location, Attack)
# Packet.data will be a class with the attributes kart_id, position, victim_id, item_id based on the command
def parse_packet(packet: Packet):
    """Parse a packet and execute the command

    Args:
        packet (Packet): The packet to parse
    """
    if packet.command == "Location":
        update_ranking(packet.data)
    elif packet.command == "Attack":
        if packet.data.victim_id == KART_ID:
            apply_item(packet.data.item_id)
    else:
        print(f"Unknown command: {packet.command}")

def read_packet():
    """Read packets from the queue and execute"""
    queue = PacketQueue(PORT)
    while True:
        packet = queue.recv()
        if packet is not None:
            parse_packet(packet)

def send_packet(command, data):
    """Send packets to the queue"""
    queue = PacketQueue(PORT)
    