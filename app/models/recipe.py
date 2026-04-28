from app.models.db import get_db_connection
import sqlite3

class Recipe:
    @staticmethod
    def create(user_id, title, description, ingredients, steps, image_url=None):
        """新增一篇食譜"""
        try:
            with get_db_connection() as conn:
                cursor = conn.execute(
                    '''
                    INSERT INTO recipes (user_id, title, description, ingredients, steps, image_url)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    (user_id, title, description, ingredients, steps, image_url)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in Recipe.create: {e}")
            return None

    @staticmethod
    def get_all(search_query=None):
        """取得所有食譜，支援關鍵字搜尋"""
        try:
            with get_db_connection() as conn:
                if search_query:
                    query = '''
                        SELECT r.*, u.username 
                        FROM recipes r
                        JOIN users u ON r.user_id = u.id
                        WHERE r.title LIKE ? OR r.ingredients LIKE ?
                        ORDER BY r.created_at DESC
                    '''
                    like_term = f'%{search_query}%'
                    recipes = conn.execute(query, (like_term, like_term)).fetchall()
                else:
                    query = '''
                        SELECT r.*, u.username 
                        FROM recipes r
                        JOIN users u ON r.user_id = u.id
                        ORDER BY r.created_at DESC
                    '''
                    recipes = conn.execute(query).fetchall()
                return [dict(r) for r in recipes]
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(recipe_id):
        """根據 ID 取得單篇食譜"""
        try:
            with get_db_connection() as conn:
                recipe = conn.execute(
                    '''
                    SELECT r.*, u.username 
                    FROM recipes r
                    JOIN users u ON r.user_id = u.id
                    WHERE r.id = ?
                    ''', 
                    (recipe_id,)
                ).fetchone()
                return dict(recipe) if recipe else None
        except sqlite3.Error as e:
            print(f"Database error in Recipe.get_by_id: {e}")
            return None

    @staticmethod
    def update(recipe_id, user_id, title, description, ingredients, steps, image_url=None):
        """更新自己的食譜"""
        try:
            with get_db_connection() as conn:
                conn.execute(
                    '''
                    UPDATE recipes 
                    SET title = ?, description = ?, ingredients = ?, steps = ?, image_url = ?
                    WHERE id = ? AND user_id = ?
                    ''',
                    (title, description, ingredients, steps, image_url, recipe_id, user_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in Recipe.update: {e}")
            return False

    @staticmethod
    def delete(recipe_id, user_id):
        """刪除自己的食譜"""
        try:
            with get_db_connection() as conn:
                conn.execute('DELETE FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in Recipe.delete: {e}")
            return False
