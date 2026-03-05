import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Khởi tạo các đối tượng dùng chung
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 1. Nạp cấu hình từ file config.py
    from config import Config
    app.config.from_object(Config)
    
    # 2. Kết nối các thư viện với app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # Trỏ về trang đăng nhập của Blueprint auth

    # 3. Đăng ký các Blueprint (Kết nối các file routes)
    from auth import auth_bp
    from admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # 4. Tự động tạo bảng Database và tài khoản Admin mẫu
    with app.app_context():
        import models 
        try:
            db.create_all()
            # Kiểm tra nếu chưa có Admin thì tạo một cái để test
            admin_check = models.User.query.filter_by(role='admin').first()
            if not admin_check:
                from werkzeug.security import generate_password_hash
                new_admin = models.User(
                    username='admin',
                    email='admin@gmail.com',
                    password=generate_password_hash('admin123'),
                    role='admin'
                )
                db.session.add(new_admin)
                db.session.commit()
                print(">>> Đã tạo tài khoản Admin mặc định: admin / admin123")
        except Exception as e:
            print(f">>> Lỗi khi khởi tạo Database: {e}")

    # 5. Route trang chủ (Tránh lỗi 404 khi vào domain chính)
    @app.route('/')
    def index():
        return render_template('index.html')

    return app

# Đối tượng app dành cho Gunicorn (Render sẽ gọi cái này)
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)