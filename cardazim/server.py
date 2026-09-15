import argparse
import socket
import sys
import threading as t

def get_message(conn: socket.socket) -> str:
    """
    Gets the message sent by the client.
    """
    
    message_length = int.from_bytes(conn.recv(4), byteorder='little') # Get the message length (first four bytes)

    data = conn.recv(message_length) # Recieve the data
    msg = data.decode() # Decode the message

    return msg

def handle_connection(conn: socket.socket):
    """
    Prints the client data and then closes the connection.
    """
    
    msg = get_message(conn) # Gets the message
    print(f"Recieved data: {msg}")

    conn.close() # Close the connection

def create_handler(conn: socket.socket):
    """
    Creates a thread which handles the connection.
    """

    thread = t.Thread(target=handle_connection, args=(conn,))
    thread.start()

def run_server(ip: str, port: int):
    """
    Starts the server which listens for messages and then prints them.
    """

    # Create a socket connection and listen on the ip and port
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.bind((ip, port))
    serv.listen(5)

    while True:
        conn, _ = serv.accept() # Accept a connection

        create_handler(conn)

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