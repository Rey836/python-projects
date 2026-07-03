"""
crypto.py

Provides encryption and decryption for the password manager.
"""

import base64
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class CryptoManager:
    """Handles encryption, decryption, and key derivation."""

    def generate_salt(self) -> bytes:
        """Generate a cryptographically secure random salt."""
        return os.urandom(16)

    def derive_key(self, master_password: str, salt: bytes) -> bytes:
        """
        Derive a Fernet-compatible key from the user's master password.
        """

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=390000,
        )

        key = base64.urlsafe_b64encode(
            kdf.derive(master_password.encode())
        )

        return key

    def encrypt(self, plaintext: str, key: bytes) -> bytes:
        """Encrypt plaintext."""

        cipher = Fernet(key)

        return cipher.encrypt(
            plaintext.encode()
        )

    def decrypt(self, encrypted_data: bytes, key: bytes) -> str:
        """Decrypt encrypted data."""

        cipher = Fernet(key)

        return cipher.decrypt(
            encrypted_data
        ).decode()