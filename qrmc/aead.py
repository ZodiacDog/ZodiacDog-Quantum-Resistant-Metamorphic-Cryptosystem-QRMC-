"""
Optional wrapper around the vetted `cryptography` library's AES-GCM.

This is classical authenticated encryption. It is not post-quantum.
Prefer this over qrmc.experimental when you need a real AEAD in tests
or local tooling. It is still not a complete production cryptosystem
(no key lifecycle, no protocol, no audit).
"""

from __future__ import annotations

import secrets

MAGIC = b"QRMCA1"
NONCE_LEN = 12


def _aesgcm(key: bytes):
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise ImportError(
            "The optional AEAD wrapper requires the 'cryptography' package. "
            "Install with: pip install 'qrmc[aead]'  or  pip install cryptography"
        ) from exc
    return AESGCM(key)


class AesGcmBox:
    """AES-256-GCM wrapper. Classical AEAD, not post-quantum."""

    def __init__(self, key: bytes | None = None) -> None:
        if key is None:
            key = secrets.token_bytes(32)
        if len(key) not in (16, 24, 32):
            raise ValueError("AES key must be 16, 24, or 32 bytes")
        self.key = key
        self._aesgcm = _aesgcm(key)

    def encrypt(self, plaintext: bytes, associated_data: bytes = b"") -> bytes:
        if not isinstance(plaintext, (bytes, bytearray)):
            raise TypeError("plaintext must be bytes")
        nonce = secrets.token_bytes(NONCE_LEN)
        ct = self._aesgcm.encrypt(nonce, plaintext, associated_data)
        return MAGIC + nonce + ct

    def decrypt(self, blob: bytes, associated_data: bytes = b"") -> bytes:
        if not isinstance(blob, (bytes, bytearray)):
            raise TypeError("ciphertext must be bytes")
        if len(blob) < len(MAGIC) + NONCE_LEN + 16:
            raise ValueError("ciphertext too short")
        if blob[: len(MAGIC)] != MAGIC:
            raise ValueError("unrecognized AES-GCM ciphertext")
        nonce = blob[len(MAGIC) : len(MAGIC) + NONCE_LEN]
        ct = blob[len(MAGIC) + NONCE_LEN :]
        return self._aesgcm.decrypt(nonce, ct, associated_data)
