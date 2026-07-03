"""
Database module for Secure Password Manager.

Handles:
- Database creation
- Table creation
- CRUD operations
"""

import sqlite3
from contextlib import closing
from config import DATABASE_PATH


class DatabaseManager:
    """Manage SQLite database operations."""

    def __init__(self):
        self.db_path = DATABASE_PATH
        self.create_tables()

    def connect(self):
        """Create a database connection."""
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def create_tables(self):
        """Create required tables if they don't exist."""

        with closing(self.connect()) as conn:
            cursor = conn.cursor()

            # Users table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                salt BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
            # Password vault table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS vault(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                account_username TEXT NOT NULL,
                encrypted_password BLOB NOT NULL,
                user_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
            """)

            conn.commit()
    
    def create_user(self, username: str, password_hash: str) -> bool:
        """Insert a new user into the database"""

        try:
            with closing(self.connect()) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                INSERT INTO users(username, password_hash)
                VALUES(?, ?)
                """,
                (username, password_hash)
                )

                conn.commit()
                return True
        except Exception as e:
            print(f'database error:{e}')
            return False
        

    def get_user_by_username(self, username: str):
    
        """Retrieve a user by username."""

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            return cursor.fetchone()
        
    def add_account(
    self,
    website: str,
    account_username: str,
    encrypted_password: bytes,
    user_id: int):
        """Store a password entry."""

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO vault(
                    website,
                    account_username,
                    encrypted_password,
                    user_id
                )
                VALUES(?,?,?,?)
                """,
                (
                    website,
                    account_username,
                    encrypted_password,
                    user_id
                )
            )

            conn.commit()

    def get_accounts(self, user_id: int):

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM vault
                WHERE user_id = ?
                ORDER BY website
                """,
                (user_id,)
            )

            return cursor.fetchall()
        
    def search_website(
    self,
    website: str,
    user_id: int):

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM vault
                WHERE website = ?
                AND user_id = ?
                """,
                (
                    website,
                    user_id
                )
            )

            return cursor.fetchone()
        
    def delete_account(
    self,
    account_id: int):

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM vault
                WHERE id = ?
                """,
                (account_id,)
            )

            conn.commit()

    def update_password(
    self,
    account_id: int,
    encrypted_password: bytes):

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE vault
                SET encrypted_password = ?
                WHERE id = ?
                """,
                (
                    encrypted_password,
                    account_id
                )
            )

            conn.commit()

    def get_user_by_username(self, username: str):
        """
        Retrieve a user by username.
        """

        with closing(self.connect()) as conn:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM users
                WHERE username = ?
                """,
                (username,)
            )

            return cursor.fetchone()