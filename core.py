"""
truerng.core
~~~~~~~~~~~~
True random number generation using OS-level entropy (os.urandom),
which pulls from hardware entropy sources like /dev/urandom on Linux/macOS
and CryptGenRandom on Windows — not a predictable PRNG.
"""

import os
import struct
import math


def _urandom_bytes(n: int) -> bytes:
    """Pull n bytes from the OS entropy pool."""
    if n < 1:
        raise ValueError("n must be at least 1")
    return os.urandom(n)


def random_bytes(n: int) -> bytes:
    """
    Return n truly random bytes.

    Args:
        n: Number of bytes to generate.

    Returns:
        bytes of length n.

    Example:
        >>> random_bytes(16)
        b'\\x3f\\xa1...'
    """
    return _urandom_bytes(n)


def random_int(low: int, high: int) -> int:
    """
    Return a truly random integer in the range [low, high] (inclusive).

    Uses rejection sampling over os.urandom to avoid modulo bias.

    Args:
        low:  Lower bound (inclusive).
        high: Upper bound (inclusive).

    Returns:
        A random int between low and high.

    Example:
        >>> random_int(1, 6)   # fair die roll
        4
    """
    if low > high:
        raise ValueError(f"low ({low}) must be <= high ({high})")
    if low == high:
        return low

    span = high - low + 1
    # Number of bits needed to represent span
    bits = span.bit_length()
    byte_count = math.ceil(bits / 8)
    # Rejection threshold to eliminate bias
    threshold = (256 ** byte_count) % span

    while True:
        raw = _urandom_bytes(byte_count)
        val = int.from_bytes(raw, "big")
        if val >= threshold:
            return low + (val % span)


def random_float() -> float:
    """
    Return a truly random float in [0.0, 1.0).

    Uses 8 bytes of entropy mapped to a 64-bit unsigned int,
    then divided by 2^64.

    Returns:
        A float in [0.0, 1.0).

    Example:
        >>> random_float()
        0.37291048...
    """
    raw = _urandom_bytes(8)
    val = int.from_bytes(raw, "big")
    return val / (2 ** 64)


def random_float_range(low: float, high: float) -> float:
    """
    Return a truly random float in [low, high).

    Args:
        low:  Lower bound (inclusive).
        high: Upper bound (exclusive).

    Returns:
        A float in [low, high).

    Example:
        >>> random_float_range(1.5, 9.5)
        6.238...
    """
    if low >= high:
        raise ValueError(f"low ({low}) must be < high ({high})")
    return low + random_float() * (high - low)


def random_choice(seq):
    """
    Return a truly random element from a non-empty sequence.

    Args:
        seq: Any subscriptable sequence (list, tuple, string, etc.)

    Returns:
        One element chosen at random.

    Example:
        >>> random_choice(['heads', 'tails'])
        'tails'
    """
    if not seq:
        raise ValueError("Cannot choose from an empty sequence")
    return seq[random_int(0, len(seq) - 1)]


def random_shuffle(seq: list) -> list:
    """
    Return a new list with elements of seq shuffled using true randomness.
    Uses a Fisher-Yates shuffle driven by os.urandom.

    Args:
        seq: A list to shuffle.

    Returns:
        A new shuffled list (original is not modified).

    Example:
        >>> random_shuffle([1, 2, 3, 4, 5])
        [3, 1, 5, 2, 4]
    """
    result = list(seq)
    for i in range(len(result) - 1, 0, -1):
        j = random_int(0, i)
        result[i], result[j] = result[j], result[i]
    return result


def random_sample(seq, k: int) -> list:
    """
    Return k unique elements chosen at random from seq.

    Args:
        seq: Source sequence.
        k:   Number of elements to pick.

    Returns:
        A list of k unique elements.

    Example:
        >>> random_sample(range(100), 5)
        [42, 7, 91, 3, 55]
    """
    pool = list(seq)
    if k > len(pool):
        raise ValueError(f"k ({k}) is larger than the population ({len(pool)})")
    return random_shuffle(pool)[:k]


def random_hex(n_bytes: int = 16) -> str:
    """
    Return a random hex string (2 * n_bytes characters long).

    Useful for tokens, IDs, nonces.

    Args:
        n_bytes: Number of random bytes (default 16 → 32 hex chars).

    Returns:
        Hex string.

    Example:
        >>> random_hex()
        'a3f1c9e2...'
    """
    return _urandom_bytes(n_bytes).hex()


def random_token(n_bytes: int = 32) -> str:
    """
    Return a URL-safe random token using base64 encoding.

    Args:
        n_bytes: Entropy size in bytes.

    Returns:
        A URL-safe base64 string (without padding).

    Example:
        >>> random_token()
        'X9kLmP3...'
    """
    import base64
    raw = _urandom_bytes(n_bytes)
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")
