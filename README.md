# truerng

A Python library for generating truly random numbers using OS-level entropy.

Python's built-in `random` module uses the **Mersenne Twister** — a pseudorandom number generator (PRNG). Given the same seed, it produces the same sequence every time. It's fast, but predictable. For anything security-sensitive (tokens, keys, simulations, lotteries), you need better.

`truerng` pulls from **`os.urandom`**, which is backed by:
- `/dev/urandom` on Linux/macOS (seeded by hardware entropy: CPU jitter, device interrupts, etc.)
- `CryptGenRandom` on Windows

No seed. No repeatable sequence. No prediction.

---

## Installation

```bash
pip install truerng
```

Or from source:

```bash
git clone https://github.com/yourusername/truerng
cd truerng
pip install .
```

---

## Quick Start

```python
from truerng import random_int, random_float, random_choice, random_token

# Fair die roll
print(random_int(1, 6))

# Float between 0.0 and 1.0
print(random_float())

# Pick a winner
print(random_choice(['Alice', 'Bob', 'Charlie']))

# Secure session token
print(random_token())
```

---

## API Reference

### `random_bytes(n: int) -> bytes`
Returns `n` truly random bytes directly from the OS entropy pool.

```python
random_bytes(16)  # b'\x3f\xa1...'
```

---

### `random_int(low: int, high: int) -> int`
Returns a random integer in `[low, high]` (both inclusive).
Uses **rejection sampling** to eliminate modulo bias.

```python
random_int(1, 100)   # e.g. 42
random_int(0, 1)     # coin flip
```

---

### `random_float() -> float`
Returns a random float in `[0.0, 1.0)`.
Mapped from 64 bits of entropy — not a PRNG output.

```python
random_float()  # e.g. 0.7312948...
```

---

### `random_float_range(low: float, high: float) -> float`
Returns a random float in `[low, high)`.

```python
random_float_range(1.5, 9.5)  # e.g. 6.238...
```

---

### `random_choice(seq) -> any`
Returns one element from a sequence, chosen at random.

```python
random_choice(['rock', 'paper', 'scissors'])
random_choice('ABCDEF')
```

---

### `random_shuffle(seq: list) -> list`
Returns a **new** shuffled list using Fisher-Yates driven by true entropy.
The original sequence is not modified.

```python
random_shuffle([1, 2, 3, 4, 5])  # e.g. [3, 1, 5, 2, 4]
```

---

### `random_sample(seq, k: int) -> list`
Returns `k` unique elements chosen at random from `seq`.

```python
random_sample(range(100), 5)  # e.g. [42, 7, 91, 3, 55]
```

---

### `random_hex(n_bytes: int = 16) -> str`
Returns a hex string of length `2 * n_bytes`.
Useful for IDs and nonces.

```python
random_hex()     # 32-char hex string
random_hex(8)    # 16-char hex string
```

---

### `random_token(n_bytes: int = 32) -> str`
Returns a URL-safe base64 token without padding.
Ideal for session tokens, API keys, CSRF tokens.

```python
random_token()   # e.g. 'X9kLmP3qRs...'
```

---

## Why not just use `secrets`?

Python's built-in [`secrets`](https://docs.python.org/3/library/secrets.html) module (added in 3.6) also uses `os.urandom` and is great for cryptographic use. `truerng` provides a richer API surface — float ranges, shuffles, samples — with the same entropy source, zero dependencies, and a focus on being easy to understand and extend.

---

## Running Tests

```bash
pip install pytest
pytest tests/
```

---

## License

MIT
