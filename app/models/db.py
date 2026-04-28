import sqlite3
import os

# 預設資料庫路徑：指向 instance/database.db
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'instance', 'database.db')

def get_db_connection():
    """取得 SQLite 資料庫連線，並將結果轉換為 dict 形式存取"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 開啟 Foreign Key 支援
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def init_db():
    """初始化資料庫（執行 schema.sql）"""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'database', 'schema.sql')
    
    # 如果 instance 目錄不存在則建立
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    with get_db_connection() as conn:
        with open(schema_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
