import struct

FORMAT_STRING = "<I"

def encode_string(string: str) -> bytes:
    return struct.pack(FORMAT_STRING, len(string)) + string.encode()