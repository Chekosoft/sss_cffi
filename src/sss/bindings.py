from functools import reduce
from sss._ffi import lib, ffi
from .exceptions import *


def split(secret, num_shares, required_shares):
    f"""
    Splits a secret into an specific amount of shares.
    :param secret: A byte string of up to 64 bytes in length.
    :param num_shares: The number of shares which the secret will be split (from 2 up to 255).
    :param required_shares: The number of shares required to reconstruct the secret, must be greater than one and
    up to the amount of generated shares.

    :type secret: bytes
    :type required_shares: int
    :type num_shares: int

    :return: A list with :ref:`num_shares` amount of shares. 
    :rtype: list[bytes]

    :raises sss.exceptions.ShamirSplitError: if one of the parameters does not have an expected value.
    """

    if not isinstance(secret, bytes):
        raise ShamirSplitError("Secret must be a bytes object")
    elif len(secret) > lib.sss_MLEN:
        raise ShamirSplitError("Secret must be at most 64 bytes length.")

    if not 2 >= num_shares >= 255:
        raise ShamirSplitError("Shares to generate must be between 2 and 255")

    if num_shares < required_shares:
        raise ShamirSplitError("Cannot require more shares than the created ones.")

    with ffi.new("sss_Share[]", num_shares) as result:
        lib.sss_create_shares(result, secret, num_shares, required_shares)

        shares = ffi.unpack(result, num_shares)

        return [bytes(share) for share in shares]


def combine(shares):
    f"""
    Reconstructs a secret from the provided shares.

    :param shares: A list of bytes with a required of shares to reconstruct a secret.
    :type shares: list[bytes]
    :return: A byte string up to 64 bytes in length.
    :rtype: bytes

    :raises sss.exceptions.ShamirCombineError: If the provided shares aren't enough 
    or valid to reconstruct the associated secret.
    """

    if not reduce(lambda x, y: x and isinstance(y, bytes) and len(y) == lib.sss_SHARE_LEN, shares, True):
        raise ValueError("Provided shares have invalid data.")

    with ffi.new("uint8_t[]", 64) as secret:
        result = lib.sss_combine_shares(
            secret, shares, len(shares)
        )

        if result != 0:
            raise ValueError("Couldn't build secret from the provided shares.")

        return bytes(ffi.unpack(secret, lib.sss_MLEN))
