"""
vault.py

Handles all password vault operations.

Responsibilities:
- Add password
- View passwords
- Search passwords
- Update passwords
- Delete passwords
"""

from database import DatabaseManager
from crypto import CryptoManager
from models import User


class VaultManager:
    """Handles password vault operations."""

    def __init__(self):
        self.db = DatabaseManager()
        self.crypto = CryptoManager()