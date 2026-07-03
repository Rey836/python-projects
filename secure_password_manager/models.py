"""
models.py

Data models used throughout the application.
"""

from dataclasses import dataclass


@dataclass
class User:
    """
    Represents an authenticated user.
    """

    id: int
    username: str
    salt: bytes
    encryption_key: bytes