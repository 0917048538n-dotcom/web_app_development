from flask import render_template, request, redirect, url_for, session, flash
from . import auth_bp

@auth_bp.route('/register', methods=['GET'])
def register_page():
    """顯示註冊表單"""
    pass

@auth_bp.route('/register', methods=['POST'])
def register_process():
    """接收表單資料，建立新使用者並寫入資料庫"""
    pass

@auth_bp.route('/login', methods=['GET'])
def login_page():
    """顯示登入表單"""
    pass

@auth_bp.route('/login', methods=['POST'])
def login_process():
    """驗證使用者帳密，成功後將 user_id 寫入 session"""
    pass

@auth_bp.route('/logout', methods=['GET'])
def logout():
    """清除 session 中的使用者資訊並登出"""
    pass
