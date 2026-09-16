import struct

class MockSocket:
    sent_data = []
    addr = None

    def __init__(self, a, b) -> None:
        pass

    def connect(self, addr):
        MockSocket.addr = addr

    def send(self, data: bytes):
        MockSocket.sent_data.append(data)

    def recv(self, num: int) -> bytes:
        return struct.pack('I', num)

    def close(self):
        pass