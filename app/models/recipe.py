from app.models.db import get_db_connection

class Recipe:
    @staticmethod
    def create(user_id, title, description, ingredients, steps, image_url=None):
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

    @staticmethod
    def get_by_id(recipe_id):
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

    @staticmethod
    def get_all(search_query=None):
        with get_db_connection() as conn:
            if search_query:
                # 簡單的關鍵字搜尋
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

    @staticmethod
    def delete(recipe_id, user_id):
        # 確保只能刪除自己的食譜
        with get_db_connection() as conn:
            conn.execute('DELETE FROM recipes WHERE id = ? AND user_id = ?', (recipe_id, user_id))
            conn.commit()
