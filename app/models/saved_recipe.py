from app.models.db import get_db_connection

class SavedRecipe:
    @staticmethod
    def save(user_id, recipe_id):
        with get_db_connection() as conn:
            try:
                conn.execute(
                    'INSERT INTO saved_recipes (user_id, recipe_id) VALUES (?, ?)',
                    (user_id, recipe_id)
                )
                conn.commit()
                return True
            except conn.IntegrityError:
                # 已經收藏過了，或者是 FK 失敗
                return False

    @staticmethod
    def unsave(user_id, recipe_id):
        with get_db_connection() as conn:
            conn.execute(
                'DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?',
                (user_id, recipe_id)
            )
            conn.commit()

    @staticmethod
    def get_by_user(user_id):
        with get_db_connection() as conn:
            recipes = conn.execute(
                '''
                SELECT r.*, u.username 
                FROM saved_recipes sr
                JOIN recipes r ON sr.recipe_id = r.id
                JOIN users u ON r.user_id = u.id
                WHERE sr.user_id = ?
                ORDER BY sr.created_at DESC
                ''',
                (user_id,)
            ).fetchall()
            return [dict(r) for r in recipes]
    
    @staticmethod
    def is_saved(user_id, recipe_id):
        with get_db_connection() as conn:
            result = conn.execute(
                'SELECT 1 FROM saved_recipes WHERE user_id = ? AND recipe_id = ?',
                (user_id, recipe_id)
            ).fetchone()
            return bool(result)
