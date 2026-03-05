from flask import Blueprint, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user
from models import db, User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # 1. Kiểm tra user tồn tại
    if User.query.filter_by(username=username).first():
        return "Tên đăng nhập đã tồn tại!", 400

    # 2. Tạo user mới và lưu vào DB
    hashed_pw = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_pw)
    
    db.session.add(new_user)
    db.session.commit()

    # --- BƯỚC QUAN TRỌNG: TỰ ĐỘNG ĐĂNG NHẬP ---
    # Sau khi commit, new_user đã có ID từ SQL Server, ta dùng nó để đăng nhập luôn
    login_user(new_user)

    # 3. Chuyển hướng về trang chủ (Lúc này current_user đã có dữ liệu)
    return redirect(url_for('index'))

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        # KIỂM TRA TRẠNG THÁI KHÓA
        if not user.is_active_account:
            return "Tài khoản của bạn đã bị khóa! Vui lòng liên hệ Admin.", 403
            
        login_user(user)
        return redirect(url_for('index'))
    
    return "Sai thông tin đăng nhập!", 401
@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))