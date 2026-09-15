import struct

FORMAT_STRING = "<I"
INT_SIZE = 4

def encode_string(string: str) -> bytes:
    return struct.pack(FORMAT_STRING, len(string)) + string.encode()

def decode_string(data: bytes, offset: int) -> tuple[str, int]:
    """
    Decodes a string from the bytes format.
    """

    length = struct.unpack_from(FORMAT_STRING, data, offset)[0]
    offset += struct.calcsize(FORMAT_STRING)

    string = data[offset:(offset + length)].decode()
    offset += length

    return string, offset