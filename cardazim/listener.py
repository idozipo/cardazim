import socket

from connection import Connection

class Listener:
    def __init__(self, host: str, port: int, backlog: int = 1000):
        self.host = host
        self.port = port
        self.backlog = backlog

    def __repr__(self) -> str:
        return f"Listener(port={self.port}, host={self.host}, backlog={self.backlog})"

    def __enter__(self):
        self.start()

        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

        return False

    def start(self):
        self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serv.bind((self.host, self.port))
        self.serv.listen(self.backlog)

    def stop(self):
        self.serv.close()

    def accept(self) -> Connection:
        conn, _ = self.serv.accept()

        return Connection(conn)