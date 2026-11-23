# Changelog

## Unreleased (audit fixes, 2026-11)

- Relabeled the project as an **experimental research sketch**. Removed
  unsupported post-quantum, Kyber-comparison, and “proven security” claims
  from the README.
- Added a small `qrmc` package whose experimental cipher actually
  encrypts and decrypts (stdlib only). Added tests for round-trip, tampering,
  and t-of-n secret sharing.
- Added an optional `AesGcmBox` wrapper around the vetted `cryptography`
  AES-GCM implementation (classical AEAD, not post-quantum).
- Moved the original uploaded files into `legacy/` (they do not parse, or
  `decrypt()` returned `None`).
- Added NOTICE, AUTHORS, SECURITY, `.gitignore`, and GitHub Actions CI.
- Contact updated to ml.innovation.research.lab@gmail.com, Pheba, MS.

Contributor: Korg (AI assistant, Grok Bot).

## 1.0.0-zodiacdog (2025-12)

- Initial public upload of the concept write-up and prototype scripts.
