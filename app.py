from app import create_app
from app.models.db import init_db
import os

app = create_app()

if __name__ == '__main__':
    # 啟動時自動檢查是否需要初始化資料庫
    db_path = os.path.join(app.instance_path, 'database.db')
    if not os.path.exists(db_path):
        print("Initializing database...")
        init_db()
        print("Database initialized.")
        
    app.run(debug=True)
