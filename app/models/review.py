from app.models.db import get_db_connection
import sqlite3

class Review:
    @staticmethod
    def create(user_id, recipe_id, rating, comment):
        """新增食譜評論"""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    '''
                    INSERT INTO reviews (user_id, recipe_id, rating, comment)
                    VALUES (?, ?, ?, ?)
                    ''',
                    (user_id, recipe_id, rating, comment)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in Review.create: {e}")
            return None

    @staticmethod
    def get_all():
        """取得系統所有評論"""
        try:
            with get_db_connection() as conn:
                reviews = conn.execute('SELECT * FROM reviews').fetchall()
                return [dict(r) for r in reviews]
        except sqlite3.Error as e:
            print(f"Database error in Review.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(review_id):
        """根據 ID 取得單篇評論"""
        try:
            with get_db_connection() as conn:
                review = conn.execute('SELECT * FROM reviews WHERE id = ?', (review_id,)).fetchone()
                return dict(review) if review else None
        except sqlite3.Error as e:
            print(f"Database error in Review.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_recipe(recipe_id):
        """取得特定食譜的所有評論"""
        try:
            with get_db_connection() as conn:
                reviews = conn.execute(
                    '''
                    SELECT r.*, u.username 
                    FROM reviews r
                    JOIN users u ON r.user_id = u.id
                    WHERE r.recipe_id = ?
                    ORDER BY r.created_at DESC
                    ''',
                    (recipe_id,)
                ).fetchall()
                return [dict(r) for r in reviews]
        except sqlite3.Error as e:
            print(f"Database error in Review.get_by_recipe: {e}")
            return []

    @staticmethod
    def update(review_id, user_id, rating, comment):
        """更新評論"""
        try:
            with get_db_connection() as conn:
                conn.execute(
                    'UPDATE reviews SET rating = ?, comment = ? WHERE id = ? AND user_id = ?',
                    (rating, comment, review_id, user_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in Review.update: {e}")
            return False

    @staticmethod
    def delete(review_id, user_id):
        """刪除評論"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM reviews WHERE id = ? AND user_id = ?', (review_id, user_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in Review.delete: {e}")
            return False
