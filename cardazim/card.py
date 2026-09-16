from __future__ import annotations

from os import PathLike
from typing import Union

from . import util
from .crypt_image import CryptImage

class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: str | None) -> None:
        self.name = name
        self.creator = creator
        self.image = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str:
        return f"<Card name={{{self.name}}}, creator={{{self.creator}}}>"

    def __str__(self) -> str:
        solution = "unsolved" if self.solution is None else self.solution

        return f"""
        Card {self.name} by {self.creator}
        riddle: {self.riddle}
        solution: {solution}
        """

    @classmethod
    def create_from_path(
        cls,
        name: str, 
        creator: str, 
        path: Union[str, PathLike], 
        riddle: str, 
        solution: str
    ) -> Card:
        """
        Creates a card from an image represented by its filepath.
        """

        image = CryptImage.create_from_path(path)

        return cls(
            name,
            creator,
            image,
            riddle,
            solution
        )

    def serialize(self) -> bytes:
        """ Serializes the card into a byte format. """

        return (
            util.encode_string(self.name) + \
            util.encode_string(self.creator) + \
            self.image.serialize() + \
            util.encode_string(self.riddle)
        )

    @classmethod
    def deserialize(cls, data: bytes) -> Card:
        """
        Deserializes the card from the bytes format.
        """
        offset = 0 # Initialize the offset

        name, offset = util.decode_string(data, offset)
        creator, offset = util.decode_string(data, offset)

        image, offset = CryptImage.deserialize(data, offset)

        riddle, offset = util.decode_string(data, offset)

        return cls(
            name,
            creator,
            image,
            riddle,
            None # No solution in serialization
        )

    def encrypt(self):
        """ Helper function to encrypt the image. """

        if self.solution is not None:
            self.image.encrypt(self.solution)