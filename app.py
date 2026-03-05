import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy import text # Dùng để thực thi lệnh cấu hình SQLite

# Khởi tạo db và login_manager tại đây
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
    login_manager.login_view = 'auth.login'

    # 3. Cấu hình SQLite và Tự động tạo bảng Database
    with app.app_context():
        # Ép SQLite ghi dữ liệu ngay lập tức vào file .db (tắt chế độ ghi tạm WAL)
        try:
            db.session.execute(text('PRAGMA journal_mode=DELETE;'))
            db.session.execute(text('PRAGMA synchronous=FULL;'))
        except Exception:
            pass

        import models  # Đảm bảo Flask nhận diện được các Class trong models.py
        try:
            db.create_all()
            # Tạo tài khoản Admin mặc định nếu chưa có
            admin_check = models.User.query.filter_by(role='admin').first()
            if not admin_check:
                from werkzeug.security import generate_password_hash
                admin = models.User(
                    username='admin', 
                    email='admin@gmail.com', 
                    password=generate_password_hash('admin123'),
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
            print(">>> [HỆ THỐNG] Đã khởi tạo SQLite thành công!")
        except Exception as e:
            print(f">>> [LỖI] Không thể tạo bảng: {e}")

    # 4. Đăng ký các Blueprint từ thư mục routes
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

# Đối tượng app dành cho Gunicorn (Render)
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)