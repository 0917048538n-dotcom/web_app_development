from app.models.db import get_db_connection

class Review:
    @staticmethod
    def create(user_id, recipe_id, rating, comment):
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

    @staticmethod
    def get_by_recipe(recipe_id):
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
