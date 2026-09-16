import argparse
import sys
import pathlib

import filetype

from .connection import Connection
from .card import Card

###########################################################
####################### YOUR CODE #########################
###########################################################

def send_data(server_ip: str, server_port: int, card: Card):
    '''
    Send data to server in address (server_ip, server_port).
    '''
    print(f"Sending card '{card.name}' by {card.creator}...")

    with Connection.connect(server_ip, server_port) as connection: # Create connection
        card.encrypt() # Encrypt card image
        connection.send_message(card.serialize()) # Send data
    
###########################################################
##################### END OF YOUR CODE ####################
###########################################################

def get_args():
    parser = argparse.ArgumentParser(description='Send a card to the server.')
    parser.add_argument('server_ip', type=str, help="the server's ip")
    parser.add_argument('server_port', type=int, help="the server's port")
    parser.add_argument('card_name', type=str, help='the name of the card')
    parser.add_argument('card_creator', type=str, help='the name of the card creator')
    parser.add_argument('card_riddle', type=str, help='the riddle for the card')
    parser.add_argument('card_solution', type=str, help='the solution for the card riddle')
    parser.add_argument('card_image_path', type=image_path, help='the image path for the card')
    return parser.parse_args()

def image_path(value: str) -> str:
    if not pathlib.Path(value).is_file():
        raise ValueError()

    if not filetype.is_image(value):
        raise ValueError()

    return value

def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()

    client_card = Card.create_from_path(
        args.card_name, 
        args.card_creator,
        args.card_image_path,
        args.card_riddle,
        args.card_solution
    )

    try:
        send_data(args.server_ip, args.server_port, client_card)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
