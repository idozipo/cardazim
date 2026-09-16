from __future__ import annotations

import socket

class Connection:
    def __init__(self, connection: socket.socket):
        self.sock = connection

    def __repr__(self) -> str:
        return f"<Connection from {self.sock.getsockname()} to {self.sock.getpeername()}"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close() # Close the connection

        return False

    @classmethod
    def connect(cls, host: str, port: int) -> Connection:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return cls(sock)

    def send_message(self, message: bytes):
        """ Sends a message through the connection. """
        self.sock.send(message)

    def receive_message(self) -> bytes:
        """ 
        Recieves the message from the connection.
        """

        data = b''
        while True:
            raw = self.sock.recv(4096)
            if not raw:
                break

            data += raw

        return data


    def close(self):
        self.sock.close()