import serial
import time
from construct import Struct, Int8ul, Int32ul, Const, Switch, this, Float32l, Padding, FixedSized

# Packet type tags
PING = 0
LOCATION = 1
ATTACK = 2

MAX_PACKET_SIZE = 14 # byte size of largest packet


# Common fields
Header = Struct(
    "magic" / Const(0xEFBEADDE, Int32ul),
    "tag" / Int8ul
)

# Packet body schemas
PacketBodies = {
    PING: Struct(
        "from" / Int8ul,
        "data" / Int32ul,
    ),
    LOCATION: Struct(
        "kart_id" / Int8ul,
        "x" / Float32l,
        "y" / Float32l
    ),
    ATTACK: Struct(
        "kart_id" / Int8ul,
        "item_id" / Int8ul
    )
}

# Packet structure
PacketSchema = FixedSized(MAX_PACKET_SIZE, Struct(
    "header" / Header,
    "body" / Switch(this.header.tag, PacketBodies, default=Struct())
))


# Packet wrapper class
class Packet:
    MAGIC = (0xDEADBEEF).to_bytes(4, byteorder='little')
    SIZE = MAX_PACKET_SIZE

    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.data = kwargs

    def to_bytes(self):
        return PacketSchema.build({
            "header": {"tag": self.tag},
            "body": self.data
        })

    @staticmethod
    def from_bytes(data: bytes):
        parsed = PacketSchema.parse(data)
        return Packet(parsed.header.tag, **parsed.body)

    def __repr__(self):
        return f"<Packet tag={self.tag} data={self.data}>"


class PacketQueue:
    def __init__(self, port: str, baudrate: int = 115200):
        """Opens the serial port (connected to the radio) and start comms

        Args:
            port (str): Serial port, e.g. "/dev/tty.usbmodem101"
        """
        self.port = port
        self.serial = serial.Serial(port, baudrate=baudrate)
        self.queue = bytes()


    def recv(self) -> Packet:
        """Get the latest packet from the queue, or None if there's none available within the timeout.

        Args:
            timeout (float, optional): Timeout in seconds, or None to return immediately if no packet is available.

        Returns:
            Packet: The packet at the top of the queue, or None if there is no packet.
        """
        # If there is something in the buffer, attempt to return the packet
        if self.serial.in_waiting > 0:
            self.queue += self.serial.read_all()
            print("received packet bytes:", self.queue.hex())
            start_idx = self.queue.find(0xDEADBEEF.to_bytes(4))

            # did not find the magic, return None
            if start_idx == -1:
                print("magic not found")
                return None
            # check if there's enough of a packet to return
            if len(self.queue) < start_idx + Packet.SIZE: 
                return None
            
            packet = self.queue[start_idx: start_idx + Packet.SIZE]
            self.queue = self.queue[start_idx + Packet.SIZE:]

            return packet
        
        else:
            return None



    def send(self, packet: bytes):
        """Send a packet over the network

        Args:
            packet (Packet): The packet to send
        """
        # print in little endian format
        print("sending packet bytes:", packet.hex())
        
        return self.serial.write(packet)

    def __iter__(self):
        return self
    
    def __next__(self):
        packet = self.recv(timeout=None)

        if packet is None:
            raise StopIteration
        return packet

if __name__ == "__main__":
    pq = PacketQueue("/dev/ttyACM0")
    while True:
        packet = pq.recv()
        if packet is not None:
            # print(packet.hex())
            print(Packet.from_bytes(packet))
        send_packet = Packet(LOCATION, kart_id=3, x=1.5, y=2.176)
        pq.send(send_packet.to_bytes())
        time.sleep(1) # TODO: remove this, it's just for testing purposes