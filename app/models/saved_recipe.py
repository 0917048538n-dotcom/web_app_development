from app.models.db import get_db_connection
import sqlite3

class SavedRecipe:
    @staticmethod
    def create(user_id, recipe_id):
        """新增收藏記錄 (符合 create 命名)"""
        try:
            with get_db_connection() as conn:
                conn.execute(
                    'INSERT INTO saved_recipes (user_id, recipe_id) VALUES (?, ?)',
                    (user_id, recipe_id)
                )
                conn.commit()
                return True
        except sqlite3.IntegrityError:
            # 已經收藏過了
            return False
        except sqlite3.Error as e:
            print(f"Database error in SavedRecipe.create: {e}")
            return False

    @staticmethod
    def save(user_id, recipe_id):
        """新增收藏記錄的別名"""
        return SavedRecipe.create(user_id, recipe_id)

    @staticmethod
    def delete(user_id, recipe_id):
        """移除收藏記錄"""
        try:
            with get_db_connection() as conn:
                conn.execute(
                    'DELETE FROM saved_recipes WHERE user_id = ? AND recipe_id = ?',
                    (user_id, recipe_id)
                )
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Database error in SavedRecipe.delete: {e}")
            return False

    @staticmethod
    def unsave(user_id, recipe_id):
        """移除收藏記錄的別名"""
        return SavedRecipe.delete(user_id, recipe_id)

    @staticmethod
    def get_all():
        """取得系統所有收藏記錄"""
        try:
            with get_db_connection() as conn:
                saves = conn.execute('SELECT * FROM saved_recipes').fetchall()
                return [dict(s) for s in saves]
        except sqlite3.Error as e:
            print(f"Database error in SavedRecipe.get_all: {e}")
            return []

    @staticmethod
    def get_by_id(save_id):
        """透過收藏流水號 ID 取得紀錄"""
        try:
            with get_db_connection() as conn:
                save_record = conn.execute('SELECT * FROM saved_recipes WHERE id = ?', (save_id,)).fetchone()
                return dict(save_record) if save_record else None
        except sqlite3.Error as e:
            print(f"Database error in SavedRecipe.get_by_id: {e}")
            return None

    @staticmethod
    def get_by_user(user_id):
        """取得某使用者的所有收藏"""
        try:
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
        except sqlite3.Error as e:
            print(f"Database error in SavedRecipe.get_by_user: {e}")
            return []
    
    @staticmethod
    def is_saved(user_id, recipe_id):
        """檢查是否已收藏"""
        try:
            with get_db_connection() as conn:
                result = conn.execute(
                    'SELECT 1 FROM saved_recipes WHERE user_id = ? AND recipe_id = ?',
                    (user_id, recipe_id)
                ).fetchone()
                return bool(result)
        except sqlite3.Error as e:
            print(f"Database error in SavedRecipe.is_saved: {e}")
            return False

    @staticmethod
    def update(id, data):
        """多對多關聯表不支援更新，略過"""
        pass
