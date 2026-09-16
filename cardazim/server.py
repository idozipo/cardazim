import argparse
import sys
import threading as t

from .listener import Listener
from .connection import Connection
from .card import Card

def handle_connection(conn: Connection):
    """
    Prints a single clients data and then closes the connection.
    """
    with conn:
        msg = conn.receive_message() # Gets the message
        card = Card.deserialize(msg)
        print(f"Recieved card '{card.name}' by {card.creator}")

def create_connection_handler(conn: Connection):
    """
    Creates a thread which handles a single connection.
    """

    thread = t.Thread(target=handle_connection, args=(conn,), daemon=True)
    thread.start()

def run_server(ip: str, port: int):
    """
    Starts the server which listens for messages and then prints them.
    """

    with Listener(ip, port) as listener:
        while True:
            conn = listener.accept() # Accept a connection

            create_connection_handler(conn) # Handle the connection

def get_args():
    parser = argparse.ArgumentParser(description='Listens for data from client.')
    parser.add_argument('server_ip', type=str, help="the server's ip")
    parser.add_argument('server_port', type=int, help="the server's port")
    return parser.parse_args()

def main():
    '''
    Implementation of CLI and recieving data from client.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())