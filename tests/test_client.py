import pytest
import socket
import conftest

from cardazim.card import Card
from cardazim.connection import Connection

@pytest.fixture
def mock_socket(monkeypatch):
    monkeypatch.setattr(socket, 'socket', conftest.MockSocket)

@pytest.mark.parametrize(
    ("name", 
    "creator",
    "riddle",
    "solution",
    "image"),
    [
        ("A", "B", "C", "D", "./image.png"),
        ("E", "F", "G", "H", "./image1.png"),
        ("I", "J", "K", "L", "./image2.png"),
    ]
    )
def test_card_creation(name: str, creator: str, riddle: str, solution: str, image: str):
    card = Card.create_from_path(name, creator, image, riddle, solution)

    assert name == card.name
    assert creator == card.creator
    assert riddle == card.riddle
    assert solution == card.solution

@pytest.mark.parametrize(
    ("name", 
    "creator",
    "riddle",
    "solution",
    "image"),
    [
        ("", "", "", "", "./image.png"),
        ("E", "F", "G", "H", "./image1.png"),
        ("I", "J", "K", "L", "./image2.png"),
    ]
    )
def test_card_sending(mock_socket, name: str, creator: str, riddle: str, solution: str, image: str):
    card = Card.create_from_path(name, creator, image, riddle, solution)

    with Connection.connect("127.0.0.1", 5000) as connection:
        card.encrypt()
        connection.send_message(card.serialize())

    assert conftest.MockSocket.addr == ("127.0.0.1", 5000)

    assert conftest.MockSocket.sent_data
    recieved_card = Card.deserialize(conftest.MockSocket.sent_data[0])

    assert recieved_card.name == name
    assert recieved_card.creator == creator
    assert recieved_card.riddle == riddle
    assert recieved_card.solution is None

    conftest.MockSocket.sent_data.clear()