#!/usr/bin/env python3
"""Short demo of the experimental QRMC sketch. Not for production use."""

from qrmc import ExperimentalThreshold

def main() -> None:
    print("WARNING: Experimental research sketch. Do not encrypt real data with this.")
    crypto = ExperimentalThreshold(n=5, t=3)
    message = b"Top secret: the future is metamorphic"
    ct = crypto.encrypt(message)
    print(f"Encrypted ({len(ct)} bytes): {ct[:40].hex()} ...")
    recovered = crypto.decrypt_with_shares(crypto.shares[:3], ct)
    print("Threshold decryption successful:", recovered == message)

if __name__ == "__main__":
    main()
