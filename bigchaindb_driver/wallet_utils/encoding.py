import base64
from Crypto.Hash import SHA512
import error, constants





def is_valid_address(addr):
    """
    Check if the string address is a valid Algorand address.

    Args:
        addr (str): base32 address

    Returns:
        bool: whether or not the address is valid
    """
    if not isinstance(addr, str):
        return False
    if not len(_undo_padding(addr)) == constants.address_len:
        return False
    try:
        decoded = decode_address(addr)
        if isinstance(decoded, str):
            return False
        return True
    except:
        return False


def decode_address(addr):
    """
    Decode a string address into its address bytes and checksum.

    Args:
        addr (str): base32 address

    Returns:
        bytes: address decoded into bytes

    """
    if not addr:
        return addr
    if not len(addr) == constants.address_len:
        raise error.WrongKeyLengthError
    decoded = base64.b32decode(_correct_padding(addr))
    addr = decoded[:-constants.check_sum_len_bytes]
    expected_checksum = decoded[-constants.check_sum_len_bytes:]
    chksum = _checksum(addr)

    if chksum == expected_checksum:
        return addr
    else:
        raise error.WrongChecksumError


def encode_address(addr_bytes):
    """
    Encode a byte address into a string composed of the encoded bytes and the
    checksum.

    Args:
        addr_bytes (bytes): address in bytes

    Returns:
        str: base32 encoded address
    """
    if not addr_bytes:
        return addr_bytes
    if not len(addr_bytes) == constants.key_len_bytes:
        raise error.WrongKeyBytesLengthError
    chksum = _checksum(addr_bytes)
    addr = base64.b32encode(addr_bytes+chksum)
    return _undo_padding(addr.decode())


def _checksum(addr):
    """
    Compute the checksum of size checkSumLenBytes for the address.

    Args:
        addr (bytes): address in bytes

    Returns:
        bytes: checksum of the address
    """
    return checksum(addr)[-constants.check_sum_len_bytes:]


def _correct_padding(a):
    if len(a) % 8 == 0:
        return a
    return a + "="*(8-len(a) % 8)


def _undo_padding(a):
    return a.strip("=")


def checksum(data):
    """
    Compute the checksum of arbitrary binary input.

    Args:
        data (bytes): data as bytes

    Returns:
        bytes: checksum of the data
    """
    chksum = SHA512.new(truncate="256")
    chksum.update(data)
    return chksum.digest()
