from flask import render_template, request, redirect, url_for, session, flash, abort
from . import recipe_bp

@recipe_bp.route('/', methods=['GET'])
def index():
    """首頁：顯示搜尋列與最新食譜列表"""
    pass

@recipe_bp.route('/search', methods=['GET'])
def search():
    """搜尋頁面：接收 ?q 參數並回傳搜尋結果"""
    pass

@recipe_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    """食譜詳情頁：顯示食材、步驟與所有歷史評論"""
    pass

@recipe_bp.route('/recipe/create', methods=['GET'])
def create_recipe_page():
    """顯示新增食譜表單 (需登入)"""
    pass

@recipe_bp.route('/recipe/create', methods=['POST'])
def create_recipe_process():
    """接收表單資料，寫入 recipes 資料表"""
    pass

@recipe_bp.route('/recipe/<int:recipe_id>/save', methods=['POST'])
def save_recipe(recipe_id):
    """將食譜加入個人的收藏清單 (需登入)"""
    pass

@recipe_bp.route('/recipe/<int:recipe_id>/unsave', methods=['POST'])
def unsave_recipe(recipe_id):
    """將食譜從個人的收藏清單移除 (需登入)"""
    pass

@recipe_bp.route('/recipe/<int:recipe_id>/review', methods=['POST'])
def submit_review(recipe_id):
    """接收星等與評論內容，寫入 reviews 資料表 (需登入)"""
    pass

@recipe_bp.route('/recipe/<int:recipe_id>/shopping', methods=['GET'])
def shopping_list(recipe_id):
    """單獨顯示特定食譜的食材清單，方便使用者採買時觀看"""
    pass

@recipe_bp.route('/profile', methods=['GET'])
def profile():
    """個人主頁：顯示自己建立的食譜與已收藏的食譜 (需登入)"""
    pass
