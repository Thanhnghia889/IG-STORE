from flask import Blueprint, request, redirect, url_for, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from extensions import db # Sửa import
from models import User 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        if not user.is_active_account:
            return "Tài khoản của bạn đã bị khóa!", 403
        login_user(user)
        return redirect(url_for('index'))
    return "Sai tên đăng nhập hoặc mật khẩu!", 401

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    if User.query.filter_by(username=username).first():
        return "Tên đăng nhập đã tồn tại!", 400
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('index'))

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))