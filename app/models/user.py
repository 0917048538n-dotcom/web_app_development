from app.models.db import get_db_connection

class User:
    @staticmethod
    def create(username, email, password_hash):
        with get_db_connection() as conn:
            cursor = conn.execute(
                'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                (username, email, password_hash)
            )
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def get_by_id(user_id):
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
            return dict(user) if user else None

    @staticmethod
    def get_by_email(email):
        with get_db_connection() as conn:
            user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
            return dict(user) if user else None
