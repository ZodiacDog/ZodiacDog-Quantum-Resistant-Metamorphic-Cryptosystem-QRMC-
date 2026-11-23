"""
QRMC — experimental research sketch, not a production cryptosystem.

Use ExperimentalCipher only for demos and tests. Use AesGcmBox (optional
`cryptography` extra) when you want a vetted classical AEAD. Neither is
post-quantum, and the experimental construction must not protect real data.
"""

from .experimental import (
    ExperimentalCipher,
    ExperimentalThreshold,
    combine_shares,
    split_secret,
)

__version__ = "0.2.0"
__author__ = "Michael L. McKnight / ML Innovations Research Lab"

__all__ = [
    "ExperimentalCipher",
    "ExperimentalThreshold",
    "split_secret",
    "combine_shares",
    "AesGcmBox",
    "__version__",
]


def __getattr__(name: str):
    if name == "AesGcmBox":
        from .aead import AesGcmBox

        return AesGcmBox
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
