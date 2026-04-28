from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User
from app.routes import auth_bp

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊表單"""
    if 'user_id' in session:
        return redirect(url_for('recipe.index'))
    return render_template('register.html')

@auth_bp.route('/register', methods=['POST'])
def register_process():
    """接收表單資料，建立新使用者並寫入資料庫"""
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        flash('請填寫所有欄位', 'danger')
        return redirect(url_for('auth.register_page'))

    # 檢查 email 是否已存在
    existing_user = User.get_by_email(email)
    if existing_user:
        flash('此 Email 已經註冊過', 'danger')
        return redirect(url_for('auth.register_page'))

    # 密碼加密
    password_hash = generate_password_hash(password)
    user_id = User.create(username, email, password_hash)
    
    if user_id:
        flash('註冊成功！請登入', 'success')
        return redirect(url_for('auth.login_page'))
    else:
        flash('註冊發生錯誤，請稍後再試', 'danger')
        return redirect(url_for('auth.register_page'))

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入表單"""
    if 'user_id' in session:
        return redirect(url_for('recipe.index'))
    return render_template('login.html')

@auth_bp.route('/login', methods=['POST'])
def login_process():
    """驗證使用者帳密，成功後將 user_id 寫入 session"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email or not password:
        flash('請填寫所有欄位', 'danger')
        return redirect(url_for('auth.login_page'))

    user = User.get_by_email(email)
    
    if user and check_password_hash(user['password_hash'], password):
        session['user_id'] = user['id']
        session['username'] = user['username']
        flash('登入成功', 'success')
        return redirect(url_for('recipe.index'))
    else:
        flash('Email 或密碼錯誤', 'danger')
        return redirect(url_for('auth.login_page'))

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """清除 session 中的使用者資訊並登出"""
    session.clear()
    flash('您已成功登出', 'info')
    return redirect(url_for('recipe.index'))
