from __future__ import annotations

import socket

class Connection:
    def __init__(self, connection: socket.socket) -> None:
        self.sock = connection

    def __repr__(self) -> str:
        return f"<Connection from {self.sock.getsockname()} to {self.sock.getpeername()}"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close() # Close the connection

        return True

    @classmethod
    def connect(cls, host: str, port: int) -> Connection:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return cls(sock)

    def send_message(self, message: bytes):
        """ Sends a message through the connection. """
        self.sock.send(message)

    def recieve_message(self) -> bytes:
        """ 
        Recieves the message from the connection.
        """

        msg = b''
        while True:
            data = self.sock.recv(4096) # Recieve 4kb at a time.
            if not data:
                break # No more data.

            msg += data

        return msg

    def close(self):
        self.sock.close()