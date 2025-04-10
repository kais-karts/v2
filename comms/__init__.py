import serial
import threading
import time

class Packet:
    """
    TODO
    """
    # These discriminants MUST match the ones in /comms/include/packet.h/Packet::tag
    PING = 0
    LOCATION = 1
    ATTACK = 2

    SIZE = 4 # TODO: size of the packet in bytes, change to not just be a constant

    def __init__(self, tag: int, **data):
        self.tag = tag
        self.__dict__.update(data)

    def parse(bytes):
        raise NotImplementedError("TODO")


class PacketQueue:
    def __init__(self, port: str, baudrate: int = 115200):
        """Opens the serial port (connected to the radio) and start comms

        Args:
            port (str): Serial port, e.g. "/dev/tty.usbmodem101"
        """
        self.port = port
        self.serial = serial.Serial(port, baudrate=baudrate)
        self.queue = []

        # start a thread which reads from the serial port and adds packets to the queue
        self.thread = threading.Thread(target=self._read_serial)
        self.thread.start()


    def _read_serial(self):
        """Read from the serial port and add packets to the queue"""
        while True:
            # read a packet from the serial port
            packet = self.serial.read(Packet.SIZE)
            if packet:
                # parse the packet and add it to the queue
                self.queue.append(Packet.parse(packet))

    def recv(self, timeout=None) -> Packet:
        """Get the latest packet from the queue, or None if there's none available within the timeout.

        Args:
            timeout (float, optional): Timeout in seconds, or None to return immediately if no packet is available.

        Returns:
            Packet: The packet at the top of the queue, or None if there is no packet.
        """
        # wait for a packet to be available, or timeout
        start_time = time.time() # seconds
        while timeout is None or (time.time() - start_time) < timeout:
            if self.queue:
                break
            
        # return the packet at the top of the queue, or None if there is no packet
        return self.queue.pop(0) if self.queue else None

    def send(self, packet: Packet):
        """Send a packet over the network

        Args:
            packet (Packet): The packet to send
        """
        return self.serial.write(packet)

    def __iter__(self):
        return self
    
    def __next__(self):
        packet = self.recv(timeout=None)

        if packet is None:
            raise StopIteration
        return packet