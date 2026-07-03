"""
auth.py

Authentication module for the Secure Password Manager.

Responsibilities:
- Register new users
- Authenticate existing users
- Generate and store user salts
- Hash master passwords using Argon2
- Derive encryption keys after successful login
"""
from models import User
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from database import DatabaseManager
from crypto import CryptoManager


class AuthManager:
    """Handles user registration and authentication."""

    def __init__(self):
        """Initialize required managers."""
        self.db = DatabaseManager()
        self.crypto = CryptoManager()
        self.hasher = PasswordHasher()

    def register(self, username: str, master_password: str) -> bool:
        """
        Register a new user.

        Args:
            username: The user's unique username.
            master_password: The user's master password.

        Returns:
            True if registration succeeds.

        Raises:
            ValueError: If the username already exists.
        """

        # Check if username already exists
        existing_user = self.db.get_user_by_username(username)

        if existing_user:
            raise ValueError("Username already exists.")

        # Generate a unique salt
        salt = self.crypto.generate_salt()

        # Hash the master password using Argon2
        password_hash = self.hasher.hash(master_password)

        # Save the new user
        self.db.create_user(
            username=username,
            password_hash=password_hash,
            salt=salt
        )

        return True

    def login(self, username: str, master_password: str):
        """
        Authenticate a user and derive the encryption key.
        """

        # Find the user
        user = self.db.get_user_by_username(username)

        if user is None:
            raise ValueError("User does not exist.")

        try:
            # Verify the Argon2 password hash
            self.hasher.verify(
                user["password_hash"],
                master_password
            )

        except VerifyMismatchError:
            raise ValueError("Invalid username or password.")

        # Derive the encryption key using the stored salt
        encryption_key = self.crypto.derive_key(
            master_password,
            user["salt"]
        )

        return User(
            id=user["id"],
            username=user["username"],
            salt=user["salt"],
            encryption_key=encryption_key
        )