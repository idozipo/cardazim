import argparse
import sys
import socket
import struct


###########################################################
####################### YOUR CODE #########################
###########################################################

def encode_data(data: str) -> bytes:
    """
    Encodes data in expected format.
    """
    return struct.pack(f'<I{len(data)}s', len(data), data.encode())

def send_data(server_ip: str, server_port: int, data: str):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    print("Sending message...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create socket
    sock.connect((server_ip, server_port)) # Create connection
    sock.send(encode_data(data)) # Send data
    
###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str, help="the server's ip")
    parser.add_argument('server_port', type=int, help="the server's port")
    parser.add_argument('data', type=str, help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
