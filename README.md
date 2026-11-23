# QRMC — experimental research sketch

**Do not use this software to encrypt real data.**

This repository is a research sketch by [ML Innovations Research Lab](https://github.com/ZodiacDog)
(Michael L. McKnight, Pheba, Mississippi). It is **not** a production
cryptosystem, **not** post-quantum, and **not** a drop-in replacement for
Kyber, Dilithium, or any NIST PQC algorithm.

Earlier versions of this README described category-theoretic, TQFT, and
“Kolmogorov / halting-problem” security, published a comparison table
against Kyber-768, and used language such as “proven #P-complete” and
“unconditional security.” **Those claims were not supported by the code**
and have been withdrawn. The original scripts also did not work as
advertised: `metamorphic_pqc.py` did not parse under Python 3, and
`decrypt()` in the “ZodiacDog Edition” always returned `None`.

The 2026 audit kept those files in [`legacy/`](legacy/) for history and
replaced them with a small, tested package that actually round-trips.

## What this repo contains now

| Piece | What it is | What it is not |
|---|---|---|
| `qrmc.ExperimentalCipher` | A stdlib encrypt-then-MAC toy that **round-trips** and rejects bit flips | A secure, reviewed, or post-quantum cipher |
| `qrmc.ExperimentalThreshold` | Educational Shamir (GF(256)) splitting of that toy’s secret | A production threshold PKE |
| `qrmc.AesGcmBox` (optional) | A thin wrapper around the vetted `cryptography` **AES-GCM** implementation | Post-quantum; a complete protocol |

If you need real cryptography, use a reviewed library (`cryptography`,
libsodium, or a NIST PQC implementation such as liboqs). Do not invent a
wrapper and call it “quantum-resistant.”

## Install

```bash
git clone https://github.com/ZodiacDog/ZodiacDog-Quantum-Resistant-Metamorphic-Cryptosystem-QRMC-.git
cd ZodiacDog-Quantum-Resistant-Metamorphic-Cryptosystem-QRMC-
pip install -e ".[dev]"    # tests + optional AES-GCM wrapper
```

Python 3.10+ is required. The experimental cipher has **no required
dependencies**. The AES-GCM wrapper needs `cryptography`.

## Quick start

```python
from qrmc import ExperimentalCipher, ExperimentalThreshold

# Toy symmetric round-trip (NOT secure)
box = ExperimentalCipher()
token = box.encrypt(b"lab demo only")
assert box.decrypt(token) == b"lab demo only"

# Educational 3-of-5 sharing of the toy secret
thresh = ExperimentalThreshold(n=5, t=3)
ct = thresh.encrypt(b"lab demo only")
assert thresh.decrypt_with_shares(thresh.shares[:3], ct) == b"lab demo only"
```

Optional classical AEAD (not post-quantum):

```python
from qrmc import AesGcmBox  # requires: pip install 'qrmc[aead]'

box = AesGcmBox()
token = box.encrypt(b"lab demo only")
assert box.decrypt(token) == b"lab demo only"
```

Or: `python -m qrmc` / `python examples/demo.py`.

## Tests

```bash
python -m pytest -q
```

On the 2026-11 audit machine (Python 3.13, with `cryptography` installed)
the suite was **10 passed, 0 failed**. Re-run locally for current counts.

## License

Apache License 2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).

Developed and created by ML Innovations Research Lab (Michael L. McKnight).
Contributor: Korg (AI assistant, Grok Bot) — audit fixes listed in
[CHANGELOG.md](CHANGELOG.md).

## Contact

**M. L. McKnight**  
ML Innovations Research Lab  
Pheba, Mississippi  

Email: [ml.innovation.research.lab@gmail.com](mailto:ml.innovation.research.lab@gmail.com)
