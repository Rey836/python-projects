"""
Configuration settings for Secure Password Manager.
"""

from pathlib import Path

# Project Directories

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# Database

DATABASE_NAME = "vault.db"
DATABASE_PATH = DATA_DIR / DATABASE_NAME

# Logging

LOG_FILE = LOG_DIR / "app.log"

# Security

PASSWORD_MIN_LENGTH = 12

SESSION_TIMEOUT = 300  # seconds

PASSWORD_HISTORY_LIMIT = 5

# Password Generator Defaults

DEFAULT_PASSWORD_LENGTH = 18