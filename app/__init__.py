from flask import Flask
import os

def create_app():
    # 建立與設定 Flask app
    app = Flask(__name__, instance_relative_config=True)
    
    # 基礎設定
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev_secret_key')
    )

    # 確保 instance 資料夾存在（用於放置資料庫檔案）
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 Blueprints
    from app.routes import auth_bp, recipe_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)

    return app
