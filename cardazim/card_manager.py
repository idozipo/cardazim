from os import PathLike
from typing import Union
import hashlib
import pathlib
import json

from cardazim.card import Card

IMAGE_FILENAME = "image.jpg"
METADATA_FILENAME = "metadata.json"

UNSOLVED_DIR = "unsolved"
SOLVED_DIR = "solved"

def _image_path(dir_path: pathlib.Path):
    return dir_path / IMAGE_FILENAME

def _metadata_path(dir_path: pathlib.Path):
    return dir_path / METADATA_FILENAME

class CardManager:
    def __init__(self, dir_path: Union[str, PathLike] = '.') -> None:
        self.dir_path = dir_path

    def generate_identifier(self, card: Card) -> str:
            """ Generates a hash identifier for the card. """
    
            return 'n{' + card.name + '}c{' + card.creator + '}'
    
    def save(self, card: Card):
        """ Save the card to a directory. """
        solution_dir = UNSOLVED_DIR if card.solution is None else SOLVED_DIR

        directory = pathlib.Path(self.dir_path) / solution_dir / self.generate_identifier(card) # Full directory path

        directory.mkdir(parents=True, exist_ok=True) # Create the directory

        self._save_image(card, directory)
        self._save_metadata(card, directory)

        print(f"Saved card to path '{directory}'")

    def _save_metadata(self, card: Card, dir_path: pathlib.Path):
        """ Saves the metadata of the card to card directory. """
        with _metadata_path(dir_path).open("w") as m_file:
            contents = {
                "name": card.name,
                "creator": card.creator,
                "riddle": card.riddle,
                "solution": card.solution,
                "image_path": _image_path(dir_path).__str__()
            }

            json.dump(contents, m_file)

    def _save_image(self, card: Card, dir_path: pathlib.Path):
        """ Saves the card image to the card directory. """
        card.image.image.convert('RGB').save(_image_path(dir_path))

    def load(self, identifier: str) -> Card:
        """ Loads a card from the save file. """
        full_path = self._get_card_dir(identifier) # Get sanitized path

        name, creator, riddle, solution, image_path = self._load_meta_data(full_path)

        return Card.create_from_path(name, creator, image_path, riddle, solution)

    def _get_card_dir(self, identifier: str) -> pathlib.Path:
        """ Sanitizes the dir_path to check if such an identifier even exists. """
        solution_dirs = [SOLVED_DIR, UNSOLVED_DIR]

        # Check in both solved and unsolved dirs
        for directory in solution_dirs:
            full_path = pathlib.Path(self.dir_path) / directory / identifier

            if full_path.exists():
                return full_path

        raise FileNotFoundError("No card with that identifier exists.")

    def _load_meta_data(self, full_path: pathlib.Path) -> tuple[str, str, str, str, str]:
        with _metadata_path(full_path).open() as m_file:
            metadata = json.load(m_file)

            return (
                metadata["name"], 
                metadata["creator"], 
                metadata["riddle"], 
                metadata["solution"],
                metadata["image_path"]
            )