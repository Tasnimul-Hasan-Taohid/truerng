"""
truerng
~~~~~~~
A Python library for generating truly random numbers using OS-level entropy.

Unlike Python's built-in `random` module (which uses the Mersenne Twister PRNG
and is deterministic/predictable), truerng pulls directly from os.urandom —
backed by hardware entropy sources on every major platform.

Basic usage::

    from truerng import random_int, random_float, random_choice

    dice = random_int(1, 6)
    prob = random_float()
    winner = random_choice(['Alice', 'Bob', 'Charlie'])

"""

from truerng.core import (
    random_bytes,
    random_int,
    random_float,
    random_float_range,
    random_choice,
    random_shuffle,
    random_sample,
    random_hex,
    random_token,
)

__version__ = "0.1.0"
__author__ = "truerng contributors"

__all__ = [
    "random_bytes",
    "random_int",
    "random_float",
    "random_float_range",
    "random_choice",
    "random_shuffle",
    "random_sample",
    "random_hex",
    "random_token",
]
