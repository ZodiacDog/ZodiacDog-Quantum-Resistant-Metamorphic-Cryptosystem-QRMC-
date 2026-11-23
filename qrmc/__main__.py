"""python -m qrmc  —  run a short, honest demo."""

from .experimental import ExperimentalThreshold


def main() -> None:
    print("QRMC experimental demo")
    print("WARNING: This is a research sketch. Do not use it to encrypt real data.")
    print("The experimental construction is not secure and is not post-quantum.")
    print()
    box = ExperimentalThreshold(n=5, t=3)
    message = b"Hello from QRMC - this is a lab demo, not a product."
    ct = box.encrypt(message)
    recovered = box.decrypt_with_shares(box.shares[:3], ct)
    print(f"plaintext:  {message!r}")
    print(f"ciphertext: {len(ct)} bytes (experimental format, not a fixed 384-byte PQC token)")
    print(f"round-trip: {recovered == message}")
    try:
        from .aead import AesGcmBox

        aead = AesGcmBox()
        token = aead.encrypt(message)
        print(f"AES-GCM round-trip: {aead.decrypt(token) == message} (classical AEAD, not PQ)")
    except ImportError:
        print("AES-GCM wrapper skipped (install qrmc[aead] to try it).")


if __name__ == "__main__":
    main()
