import argparse
import socket
import sys
import threading as t

from listener import Listener

def handle_connection(listener: Listener):
    """
    Prints the client data and then closes the connection.
    """
    with listener.accept() as conn:
        msg = conn.recieve_message() # Gets the message
        print(f"Recieved data: {msg.decode()}")

def create_connection_handler(listener: Listener):
    """
    Creates a thread which handles the connection.
    """

    thread = t.Thread(target=handle_connection, args=(listener,))
    thread.start()

def run_server(ip: str, port: int):
    """
    Starts the server which listens for messages and then prints them.
    """

    with Listener(ip, port) as listener:
        while True:
            create_connection_handler(listener)

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