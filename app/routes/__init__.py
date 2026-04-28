from flask import Blueprint

# 初始化 Blueprints，讓 app.py 可以匯入並註冊
auth_bp = Blueprint('auth', __name__)
recipe_bp = Blueprint('recipe', __name__)

# 確保在初始化 Blueprint 後載入路由定義
from . import auth, recipe
