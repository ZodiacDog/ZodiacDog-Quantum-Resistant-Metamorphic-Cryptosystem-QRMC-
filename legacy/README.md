# Legacy files

These are the original 2025 uploads, kept for history.

They are **not** the supported API:

- `metamorphic_pqc.py` and `demo` do not parse under Python 3 (`b"⊥ ..."` is a syntax error) and the decrypt path did not recover plaintext.
- `ZodiacDog Edition` ran, but `decrypt()` always returned `None`.
- `NightmareDemo` is theatrical prose around homemade hashing, not a cryptosystem.

Use the `qrmc` package instead. Do not use these files to protect data.
