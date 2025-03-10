class Packet:
    """
    TODO
    """


class PacketQueue:
    def __init__(self, port: str):
        """Opens the serial port (connected to an ESP32) and start comms

        Args:
            port (str): Serial port, e.g. "/dev/tty.usbmodem101"
        """
        # TODO

    def recv(self, timeout=None) -> Packet:
        """Get the latest packet from the queue, or None if there's none available within the timeout.

        Args:
            timeout (float, optional): Timeout in seconds, or None to return immediately if no packet is available.

        Returns:
            Packet: The packet at the top of the queue, or None if there is no packet.
        """
        # TODO

    def send(self, packet: Packet):
        """Send a packet over the network

        Args:
            packet (Packet): The packet to send
        """
        # TODO