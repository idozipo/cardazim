from __future__ import annotations

import socket
import struct

class Connection:
    def __init__(self, connection: socket.socket) -> None:
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
        self.sock.send(self._encode_message(message))

    def _encode_message(self, message: bytes) -> bytes:
        """
        Encodes data in expected format.
        """
        return struct.pack(f'<I{len(message)}s', len(message), message)

    def recieve_message(self) -> bytes:
        """ 
        Recieves the message from the connection.
        """

        message_length = int.from_bytes(self.sock.recv(4), byteorder='little') # Get the message length (first four bytes)
    
        msg = self.sock.recv(message_length) # Recieve the data
    
        return msg

    def close(self):
        self.sock.close()