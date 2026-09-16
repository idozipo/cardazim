from __future__ import annotations

import hashlib
from os import PathLike
import struct
from typing import Union

from PIL import Image
from Crypto.Cipher import AES

from cardazim import util


IMAGE_SIZE_FORMAT_STR = "<II" # image_width, image_height

IMAGE_MODE_BYTES_PER_PIXEL: dict[str, int] = {
    '1': 1,
    'L': 1,
    'P': 1,
    'RGB': 3,
    'RGBA': 4,
    'CMYK': 4,
    'I': 4,
    'F': 4
} # Dictionary for converting from image mode to bytes per pixel
DEFAULT_MODE = 'RGB'

NONCE = b'arazim'
HASH_KEY_SIZE = 32
ZERO_HASH = b'\x00' * HASH_KEY_SIZE


def _hash_key(key: bytes) -> bytes:
    """ Helper function to generate a hash_key from a raw key. """
    return hashlib.sha256(key).digest()

def _get_image_mode(raw_mode: str):
    """ Helper function to validate the deserialized image mode. """

    if raw_mode not in IMAGE_MODE_BYTES_PER_PIXEL:
        return DEFAULT_MODE, IMAGE_MODE_BYTES_PER_PIXEL[DEFAULT_MODE]

    return raw_mode, IMAGE_MODE_BYTES_PER_PIXEL[raw_mode]

def _cipher_AES_on_image(image: Image.Image, key: bytes, should_encrypt: bool) -> Image.Image:
    """ 
    Helper to remove code duplication.

    Args:
        `data` - data to encrypt/decrypt
        `key` - key for AES cipher
        `should_encrypt` - if this key is true then encrypts else decrypts.
    Returns:
        Activation of the cipher on the data argument.
    """

    # Create cipher
    cipher = AES.new(key, AES.MODE_EAX, nonce=NONCE)

    # Plain image metadata
    original_image_bytes = image.tobytes()
    original_image_size = image.size
    original_image_mode = image.mode

    # Encrypt image
    cipher_image = cipher.encrypt(original_image_bytes)

    # Recreate image with encrypted data and the original image metadata
    return Image.frombytes(original_image_mode, original_image_size, cipher_image)


class CryptImage:
    def __init__(self, image: Image.Image, key_hash: bytes | None):
        self.image = image
        self.key_hash = key_hash

    @classmethod
    def create_from_path(cls, path: Union[str, PathLike]) -> CryptImage:
        image = Image.open(path)

        return cls(image, None)

    def encrypt(self, key: str):
        """
        Encrypts the image in place.
        Also, updates internal hashing values.
        """

        # Don't allow encrypting an image more than once
        if self.key_hash is not None: 
            return

        # Calculate the key for encryption
        encryption_key = _hash_key(key.encode())

        # Update internal hash
        self.key_hash = _hash_key(encryption_key)

        self.image = _cipher_AES_on_image(self.image, encryption_key, True)

    def decrypt(self, key: str) -> bool:
        """
        Decrypts the image in place.
        Also, updates internal hashing values.
        """

        # Don't allow decrypting an image more than once
        if self.key_hash is None: 
            return True # Already decrypted so success

        # Calculate the key for decryption
        encryption_key = _hash_key(key.encode())

        if _hash_key(encryption_key) != self.key_hash: # Check if key is correct
            return False

        self.key_hash = None # To signify that the image is decrypted
        
        self.image = _cipher_AES_on_image(self.image, encryption_key, False)

        return True

    def serialize(self) -> bytes:
        """ 
        Serializes the image into a byte format (including metadata).

        Format:    
                `image_width`,
                `image_height`,
                `encoded_image_mode`,
                `image_bytes`,
                `key_hash` or `ZERO_HASH` to indicate that there is no hash
        """

        return (
            struct.pack(
                IMAGE_SIZE_FORMAT_STR, 
                self.image.size[0], 
                self.image.size[1], 
            ) + \
            util.encode_string(self.image.mode) + \
            self.image.tobytes() + \
            (self.key_hash if self.key_hash else ZERO_HASH)
        )

    @classmethod
    def deserialize(cls, data: bytes, offset: int) -> tuple[CryptImage, int]:
        """
        Deserializes the CryptImage from the bytes format.
        """

        # Extract the image metadata
        width, height= struct.unpack_from(IMAGE_SIZE_FORMAT_STR, data, offset)
        offset += struct.calcsize(IMAGE_SIZE_FORMAT_STR)

        # Decode the image mode
        raw_mode, offset = util.decode_string(data, offset)
        mode, bytes_per_pixel = _get_image_mode(raw_mode) # Sanitize the raw decoded mode + gets bytes per pixel

        # Calculate the amount of bytes in the image
        data_amount = bytes_per_pixel * (width * height)

        # Recreate image from metadata + bytes
        # There are W * H pixels and each pixel is represented by 3 bytes
        image = Image.frombytes(mode, (width, height), data[offset:offset + data_amount])
        offset += data_amount

        # Extract the hash (all zeroes marks the empty hash)
        key_hash = data[offset:offset + HASH_KEY_SIZE]
        offset += HASH_KEY_SIZE

        return (cls(
            image,
            key_hash if key_hash != ZERO_HASH else None
        ), offset)
