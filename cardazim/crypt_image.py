from __future__ import annotations

import hashlib
from os import PathLike
import struct
from typing import Union

from PIL import Image
from Crypto.Cipher import AES

NONCE = b'arazim'
IMAGE_MODE = 'RGB'

class CryptImage:
    def __init__(self, image: Image.Image, key_hash: bytes | None):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]) -> CryptImage:
        image = Image.open(path)

        return cls(image, None)

    # TODO: code repetition
    # TODO: multiple encryption/decryption?
    def encrypt(self, key: str):
        encryption_key = self._hash_key(key.encode())

        # Update internal hash
        self.key_hash = self._hash_key(encryption_key)

        # Create cipher
        cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=NONCE)

        # Plain image metadata
        plain_image = self.image.tobytes()
        plain_image_size = self.image.size

        # Encrypt image
        cipher_image = cipher.encrypt(plain_image)

        # Recreate image with encrypted data and the original image metadata
        self.image = Image.frombytes(IMAGE_MODE, plain_image_size, cipher_image)

    def decrypt(self, key: str) -> bool:
        encryption_key = self._hash_key(key.encode())

        if self._hash_key(encryption_key) != self.key_hash: # Check if key is correct
            return False

        self.key_hash = None # To signify that the image is decrypted
        
        # Create cipher
        cipher = AES.new(encryption_key, AES.MODE_EAX, nonce=NONCE)

        # Cipher image metadata
        cipher_image = self.image.tobytes()
        cipher_image_size = self.image.size

        # Decrypt image
        plain_image = cipher.decrypt(cipher_image)

        # Recreate image with encrypted data and the original image metadata
        self.image = Image.frombytes(IMAGE_MODE, cipher_image_size, plain_image)

        return True

    @staticmethod
    def _hash_key(key: bytes) -> bytes:
        return hashlib.sha256(key).digest()

    def serialize(self) -> bytes:
        """ Serializes the image into a byte format (including metadata) """
        return (
            struct.pack("II", self.image.size[1], self.image.size[0]) + \
            self.image.tobytes() + \
            self.key_hash if self.key_hash else b''
        )