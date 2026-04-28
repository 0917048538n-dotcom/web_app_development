from app.models.db import get_db_connection
import sqlite3

class User:
    @staticmethod
    def create(username, email, password_hash):
        """建立新使用者"""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
                    (username, email, password_hash)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in User.create: {e}")
            return None

    @staticmethod
    def get_all():
        """取得所有使用者"""
        try:
            with get_db_connection() as conn:
                users = conn.execute('SELECT * FROM users').fetchall()
                return [dict(user) for user in users]
        except sqlite3.Error as e:
            print(f"Database error in User.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(user_id):
        """根據 ID 取得使用者"""
        try:
            with get_db_connection() as conn:
                user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
                return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_email(email):
        """根據 Email 取得使用者"""
        try:
            with get_db_connection() as conn:
                user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
                return dict(user) if user else None
        except sqlite3.Error as e:
            print(f"Database error in User.get_by_email: {e}")
            return None

    @staticmethod
    def update(user_id, username, email, password_hash):
        """更新使用者資料"""
        try:
            with get_db_connection() as conn:
                conn.execute(
                    'UPDATE users SET username = ?, email = ?, password_hash = ? WHERE id = ?',
                    (username, email, password_hash, user_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in User.update: {e}")
            return False

    @staticmethod
    def delete(user_id):
        """刪除使用者"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in User.delete: {e}")
            return False
