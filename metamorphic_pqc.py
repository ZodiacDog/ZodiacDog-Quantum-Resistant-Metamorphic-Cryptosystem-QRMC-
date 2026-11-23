"""
Backward-compatible import path.

The original file in legacy/metamorphic_pqc.py does not parse under Python 3
(non-ASCII bytes literals) and did not recover plaintext. This module wraps
the new experimental API and refuses to claim post-quantum security.
"""

from qrmc import ExperimentalThreshold as MetamorphicThresholdPQC

__all__ = ["MetamorphicThresholdPQC"]
