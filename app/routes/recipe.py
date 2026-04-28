from flask import Blueprint, render_template, request, redirect, url_for, session, flash, abort
from functools import wraps
from app.models.recipe import Recipe
from app.models.review import Review
from app.models.saved_recipe import SavedRecipe
from app.routes import recipe_bp

# --- Helper Function: 登入驗證裝飾器 ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('您需要先登入才能執行此操作', 'warning')
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return decorated_function

# --- Routes ---

@recipe_bp.route('/', methods=['GET'])
def index():
    """首頁：顯示搜尋列與最新食譜列表"""
    recipes = Recipe.get_all()
    return render_template('index.html', recipes=recipes)

@recipe_bp.route('/search', methods=['GET'])
def search():
    """搜尋頁面：接收 ?q 參數並回傳搜尋結果"""
    query = request.args.get('q', '').strip()
    recipes = Recipe.get_all(search_query=query)
    return render_template('search_results.html', recipes=recipes, query=query)

@recipe_bp.route('/recipe/<int:recipe_id>', methods=['GET'])
def recipe_detail(recipe_id):
    """食譜詳情頁：顯示食材、步驟與所有歷史評論"""
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)
        
    reviews = Review.get_by_recipe(recipe_id)
    
    # 檢查登入使用者是否已收藏此篇食譜
    is_saved = False
    if 'user_id' in session:
        is_saved = SavedRecipe.is_saved(session['user_id'], recipe_id)
        
    return render_template('recipe_detail.html', recipe=recipe, reviews=reviews, is_saved=is_saved)

@recipe_bp.route('/recipe/create', methods=['GET'])
@login_required
def create_recipe_page():
    """顯示新增食譜表單 (需登入)"""
    return render_template('recipe_create.html')

@recipe_bp.route('/recipe/create', methods=['POST'])
@login_required
def create_recipe_process():
    """接收表單資料，寫入 recipes 資料表"""
    title = request.form.get('title')
    description = request.form.get('description')
    ingredients = request.form.get('ingredients')
    steps = request.form.get('steps')
    image_url = request.form.get('image_url')
    
    if not title or not ingredients or not steps:
        flash('標題、食材與步驟為必填欄位', 'danger')
        return redirect(url_for('recipe.create_recipe_page'))
        
    recipe_id = Recipe.create(session['user_id'], title, description, ingredients, steps, image_url)
    if recipe_id:
        flash('食譜發布成功！', 'success')
        return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))
    else:
        flash('發布失敗，請稍後再試', 'danger')
        return redirect(url_for('recipe.create_recipe_page'))

@recipe_bp.route('/recipe/<int:recipe_id>/save', methods=['POST'])
@login_required
def save_recipe(recipe_id):
    """將食譜加入個人的收藏清單 (需登入)"""
    SavedRecipe.save(session['user_id'], recipe_id)
    flash('已加入收藏清單', 'success')
    return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))

@recipe_bp.route('/recipe/<int:recipe_id>/unsave', methods=['POST'])
@login_required
def unsave_recipe(recipe_id):
    """將食譜從個人的收藏清單移除 (需登入)"""
    SavedRecipe.unsave(session['user_id'], recipe_id)
    flash('已從收藏清單移除', 'info')
    return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))

@recipe_bp.route('/recipe/<int:recipe_id>/review', methods=['POST'])
@login_required
def submit_review(recipe_id):
    """接收星等與評論內容，寫入 reviews 資料表 (需登入)"""
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    
    if not rating:
        flash('請選擇評分', 'danger')
        return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))
        
    Review.create(session['user_id'], recipe_id, int(rating), comment)
    flash('評論已送出', 'success')
    return redirect(url_for('recipe.recipe_detail', recipe_id=recipe_id))

@recipe_bp.route('/recipe/<int:recipe_id>/shopping', methods=['GET'])
def shopping_list(recipe_id):
    """單獨顯示特定食譜的食材清單，方便使用者採買時觀看"""
    recipe = Recipe.get_by_id(recipe_id)
    if not recipe:
        abort(404)
    return render_template('shopping_list.html', recipe=recipe)

@recipe_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    """個人主頁：顯示自己建立的食譜與已收藏的食譜 (需登入)"""
    user_id = session['user_id']
    
    # 撈取自己發布的食譜
    all_recipes = Recipe.get_all()
    my_recipes = [r for r in all_recipes if r['user_id'] == user_id]
    
    # 撈取自己收藏的食譜
    saved_recipes = SavedRecipe.get_by_user(user_id)
    
    return render_template('profile.html', my_recipes=my_recipes, saved_recipes=saved_recipes)
