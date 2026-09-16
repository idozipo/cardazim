import argparse
import pathlib
import sys
import threading as t

from cardazim.listener import Listener
from cardazim.connection import Connection
from cardazim.card import Card
from cardazim.card_manager import CardManager

def handle_connection(conn: Connection, card_manager: CardManager):
    """
    Prints a single clients data and then closes the connection.
    """
    with conn:
        msg = conn.receive_message() # Gets the message
        card = Card.deserialize(msg)

        print("Recieved card.")
        card_manager.save(card) # Save card

def create_connection_handler(conn: Connection, card_manager: CardManager):
    """
    Creates a thread which handles a single connection.
    """

    thread = t.Thread(target=handle_connection, args=(conn,card_manager), daemon=True)
    thread.start()

def run_server(ip: str, port: int, save_dir: pathlib.Path):
    """
    Starts the server which listens for messages and then prints them.
    """

    card_manager = CardManager(save_dir)

    with Listener(ip, port) as listener:
        while True:
            conn = listener.accept() # Accept a connection

            create_connection_handler(conn, card_manager) # Handle the connection

def get_args():
    parser = argparse.ArgumentParser(description='Listens for data from client.')
    parser.add_argument('server_ip', type=str, help="the server's ip")
    parser.add_argument('server_port', type=int, help="the server's port")
    parser.add_argument('save_dir', type=directory, help="the directory to save the cards in")
    return parser.parse_args()

def directory(value) -> pathlib.Path:
    """ Validates the save directory. """
    try:
        path = pathlib.Path(value).resolve()
    except (OSError, RuntimeError):
        raise ValueError()
        
    return path

def main():
    '''
    Implementation of CLI and recieving data from client.
    '''
    args = get_args()
    try:
        run_server(args.server_ip, args.server_port, args.save_dir)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())