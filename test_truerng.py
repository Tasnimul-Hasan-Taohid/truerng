"""
Tests for truerng.
Run with: pytest tests/
"""

import pytest
from truerng import (
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


# ── random_bytes ─────────────────────────────────────────────────────────────

class TestRandomBytes:
    def test_correct_length(self):
        assert len(random_bytes(16)) == 16
        assert len(random_bytes(1)) == 1
        assert len(random_bytes(64)) == 64

    def test_returns_bytes(self):
        assert isinstance(random_bytes(8), bytes)

    def test_invalid_n(self):
        with pytest.raises(ValueError):
            random_bytes(0)

    def test_uniqueness(self):
        # Astronomically unlikely to collide across 100 draws of 16 bytes
        results = {random_bytes(16) for _ in range(100)}
        assert len(results) == 100


# ── random_int ───────────────────────────────────────────────────────────────

class TestRandomInt:
    def test_within_range(self):
        for _ in range(1000):
            v = random_int(1, 6)
            assert 1 <= v <= 6

    def test_equal_bounds(self):
        assert random_int(5, 5) == 5

    def test_invalid_range(self):
        with pytest.raises(ValueError):
            random_int(10, 5)

    def test_full_coverage(self):
        # All values 1–6 should appear within 10_000 rolls
        seen = set()
        for _ in range(10_000):
            seen.add(random_int(1, 6))
        assert seen == {1, 2, 3, 4, 5, 6}

    def test_no_modulo_bias(self):
        # Chi-squared style: counts should be roughly uniform
        counts = [0] * 6
        n = 60_000
        for _ in range(n):
            counts[random_int(0, 5)] += 1
        expected = n / 6
        for c in counts:
            # Each bucket should be within 5% of expected
            assert abs(c - expected) / expected < 0.05


# ── random_float ─────────────────────────────────────────────────────────────

class TestRandomFloat:
    def test_range(self):
        for _ in range(1000):
            v = random_float()
            assert 0.0 <= v < 1.0

    def test_uniqueness(self):
        results = {random_float() for _ in range(100)}
        assert len(results) == 100


# ── random_float_range ───────────────────────────────────────────────────────

class TestRandomFloatRange:
    def test_within_range(self):
        for _ in range(1000):
            v = random_float_range(2.5, 7.5)
            assert 2.5 <= v < 7.5

    def test_invalid_range(self):
        with pytest.raises(ValueError):
            random_float_range(5.0, 5.0)
        with pytest.raises(ValueError):
            random_float_range(9.0, 1.0)


# ── random_choice ────────────────────────────────────────────────────────────

class TestRandomChoice:
    def test_returns_member(self):
        seq = ['a', 'b', 'c', 'd']
        for _ in range(200):
            assert random_choice(seq) in seq

    def test_single_element(self):
        assert random_choice([42]) == 42

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            random_choice([])

    def test_works_with_string(self):
        assert random_choice("abc") in "abc"


# ── random_shuffle ───────────────────────────────────────────────────────────

class TestRandomShuffle:
    def test_same_elements(self):
        original = list(range(10))
        shuffled = random_shuffle(original)
        assert sorted(shuffled) == original

    def test_does_not_modify_original(self):
        original = [1, 2, 3, 4, 5]
        _ = random_shuffle(original)
        assert original == [1, 2, 3, 4, 5]

    def test_actually_shuffles(self):
        original = list(range(20))
        results = [tuple(random_shuffle(original)) for _ in range(20)]
        assert len(set(results)) > 1  # Very unlikely to all be identical


# ── random_sample ────────────────────────────────────────────────────────────

class TestRandomSample:
    def test_correct_size(self):
        assert len(random_sample(range(100), 10)) == 10

    def test_unique_elements(self):
        result = random_sample(range(100), 50)
        assert len(result) == len(set(result))

    def test_all_from_source(self):
        source = list(range(50))
        result = random_sample(source, 20)
        for v in result:
            assert v in source

    def test_k_too_large(self):
        with pytest.raises(ValueError):
            random_sample([1, 2, 3], 5)


# ── random_hex ───────────────────────────────────────────────────────────────

class TestRandomHex:
    def test_length(self):
        assert len(random_hex(16)) == 32
        assert len(random_hex(8)) == 16

    def test_is_hex(self):
        h = random_hex()
        assert all(c in '0123456789abcdef' for c in h)

    def test_uniqueness(self):
        results = {random_hex() for _ in range(100)}
        assert len(results) == 100


# ── random_token ─────────────────────────────────────────────────────────────

class TestRandomToken:
    def test_returns_string(self):
        assert isinstance(random_token(), str)

    def test_url_safe_chars(self):
        token = random_token()
        allowed = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_')
        assert all(c in allowed for c in token)

    def test_no_padding(self):
        assert '=' not in random_token()

    def test_uniqueness(self):
        results = {random_token() for _ in range(100)}
        assert len(results) == 100
