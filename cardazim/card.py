from os import PathLike
import struct
from typing import Union

from crypt_image import CryptImage

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
    ):
        image = CryptImage.create_from_path(path)

        return cls(
            name,
            creator,
            image,
            riddle,
            solution
        )

    # def serialize(self) -> bytes:
    #     len(self.name).to_bytes() + self.name.encode() + len(se)