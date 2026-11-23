# Security

**Do not use this repository to encrypt real data.**

QRMC is an experimental research sketch. The homemade `ExperimentalCipher`
is not a reviewed cryptosystem and is not post-quantum. The optional
`AesGcmBox` wrapper uses a vetted classical AEAD (AES-GCM via
`cryptography`); that wrapper is still not a complete product (no key
lifecycle, no protocol, no audit of this repo).

If you discover a bug in the example code, please open a GitHub issue or
email ml.innovation.research.lab@gmail.com. Please do not report “breaks”
of the experimental toy as if it were a deployed cryptosystem.
