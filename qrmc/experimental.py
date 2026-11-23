"""
Experimental symmetric construction used only to demonstrate a working
encrypt/decrypt round-trip and optional threshold key splitting.

THIS MODULE IS NOT SECURE. It is not post-quantum, it has not been
reviewed, and it must not be used to protect real data.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
from typing import Iterable, List, Sequence, Tuple

MAGIC = b"QRMCX1"
SESSION_LEN = 16
TAG_LEN = 32


def hkdf_sha3_256(ikm: bytes, salt: bytes, info: bytes, length: int) -> bytes:
    """HKDF (RFC 5869) with SHA3-256. Utility only; not a security claim."""
    prk = hmac.new(salt, ikm, hashlib.sha3_256).digest()
    okm = b""
    t = b""
    i = 1
    while len(okm) < length:
        t = hmac.new(prk, t + info + bytes([i]), hashlib.sha3_256).digest()
        okm += t
        i += 1
        if i > 255:
            raise ValueError("HKDF output too long")
    return okm[:length]


class ExperimentalCipher:
    """Symmetric encrypt-then-MAC toy. Not for production use."""

    def __init__(self, secret: bytes | None = None) -> None:
        if secret is None:
            secret = secrets.token_bytes(32)
        if not isinstance(secret, (bytes, bytearray)) or len(secret) < 16:
            raise ValueError("secret must be at least 16 bytes")
        self.secret = bytes(secret)

    def encrypt(self, plaintext: bytes) -> bytes:
        if not isinstance(plaintext, (bytes, bytearray)):
            raise TypeError("plaintext must be bytes")
        session = secrets.token_bytes(SESSION_LEN)
        enc_key = hkdf_sha3_256(self.secret, session, b"qrmc-exp-enc", 32)
        mac_key = hkdf_sha3_256(self.secret, session, b"qrmc-exp-mac", 32)
        stream = hashlib.shake_256(enc_key + session).digest(len(plaintext))
        ciphertext = bytes(a ^ b for a, b in zip(plaintext, stream))
        tag = hmac.new(mac_key, session + ciphertext, hashlib.sha3_256).digest()
        return MAGIC + session + tag + ciphertext

    def decrypt(self, blob: bytes) -> bytes:
        if not isinstance(blob, (bytes, bytearray)):
            raise TypeError("ciphertext must be bytes")
        if len(blob) < len(MAGIC) + SESSION_LEN + TAG_LEN:
            raise ValueError("ciphertext too short")
        if blob[: len(MAGIC)] != MAGIC:
            raise ValueError("unrecognized experimental ciphertext")
        session = blob[len(MAGIC) : len(MAGIC) + SESSION_LEN]
        tag = blob[len(MAGIC) + SESSION_LEN : len(MAGIC) + SESSION_LEN + TAG_LEN]
        ciphertext = blob[len(MAGIC) + SESSION_LEN + TAG_LEN :]
        enc_key = hkdf_sha3_256(self.secret, session, b"qrmc-exp-enc", 32)
        mac_key = hkdf_sha3_256(self.secret, session, b"qrmc-exp-mac", 32)
        expected = hmac.new(mac_key, session + ciphertext, hashlib.sha3_256).digest()
        if not hmac.compare_digest(expected, tag):
            raise ValueError("authentication failed")
        stream = hashlib.shake_256(enc_key + session).digest(len(ciphertext))
        return bytes(a ^ b for a, b in zip(ciphertext, stream))


# ---------------------------------------------------------------------------
# Educational Shamir secret sharing over GF(256). Educational only.
# ---------------------------------------------------------------------------

def _gf_mul(a: int, b: int) -> int:
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def _gf_pow(a: int, e: int) -> int:
    result = 1
    base = a
    while e:
        if e & 1:
            result = _gf_mul(result, base)
        base = _gf_mul(base, base)
        e >>= 1
    return result


def _gf_inv(a: int) -> int:
    if a == 0:
        raise ZeroDivisionError("division by zero in GF(256)")
    return _gf_pow(a, 254)


def split_secret(secret: bytes, n: int, t: int) -> List[bytes]:
    """Split `secret` into n shares, any t of which reconstruct it."""
    if not (2 <= t <= n <= 255):
        raise ValueError("need 2 <= t <= n <= 255")
    shares = [bytearray([i]) + bytearray(len(secret)) for i in range(1, n + 1)]
    for idx, byte in enumerate(secret):
        coeffs = [byte] + [secrets.randbelow(256) for _ in range(t - 1)]
        for i in range(1, n + 1):
            acc = 0
            x = 1
            for c in coeffs:
                acc ^= _gf_mul(c, x)
                x = _gf_mul(x, i)
            shares[i - 1][1 + idx] = acc
    return [bytes(s) for s in shares]


def combine_shares(shares: Sequence[bytes]) -> bytes:
    """Reconstruct a secret from at least t shares produced by split_secret."""
    if len(shares) < 2:
        raise ValueError("need at least two shares")
    length = len(shares[0]) - 1
    if length < 1 or any(len(s) != length + 1 for s in shares):
        raise ValueError("invalid or inconsistent shares")
    xs = [s[0] for s in shares]
    if len(set(xs)) != len(xs) or any(x == 0 for x in xs):
        raise ValueError("duplicate or invalid share index")
    secret = bytearray(length)
    for idx in range(length):
        acc = 0
        for i, share in enumerate(shares):
            yi = share[1 + idx]
            num = 1
            den = 1
            for j, other in enumerate(shares):
                if i == j:
                    continue
                num = _gf_mul(num, other[0])
                den = _gf_mul(den, share[0] ^ other[0])
            acc ^= _gf_mul(yi, _gf_mul(num, _gf_inv(den)))
        secret[idx] = acc
    return bytes(secret)


class ExperimentalThreshold:
    """t-of-n sharing of an ExperimentalCipher secret. Educational only."""

    def __init__(self, n: int = 5, t: int = 3, secret: bytes | None = None) -> None:
        if not (2 <= t <= n):
            raise ValueError("need 2 <= t <= n")
        self.n = n
        self.t = t
        self.cipher = ExperimentalCipher(secret)
        self.shares = split_secret(self.cipher.secret, n, t)

    def encrypt(self, plaintext: bytes) -> bytes:
        return self.cipher.encrypt(plaintext)

    def decrypt_with_shares(self, shares: Iterable[bytes], blob: bytes) -> bytes:
        share_list = list(shares)
        if len(share_list) < self.t:
            raise ValueError(f"need at least {self.t} shares")
        secret = combine_shares(share_list[: self.t])
        return ExperimentalCipher(secret).decrypt(blob)
