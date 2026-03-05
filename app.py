import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

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
    login_manager.login_view = 'login' # Tên hàm/route đăng nhập của bạn

    # 3. QUAN TRỌNG: Tự động tạo bảng Database
    # Vì Render Free không có Shell, đoạn code này sẽ làm thay việc đó
    with app.app_context():
        import models  # Đảm bảo Flask nhận diện được các Class trong models.py
        try:
            db.create_all()
            print(">>> [HỆ THỐNG] Đã khởi tạo các bảng SQLite thành công!")
        except Exception as e:
            print(f">>> [LỖI] Không thể tạo bảng: {e}")

    # 4. Đăng ký các Route (Nếu bạn để route trong file khác, hãy import ở đây)
    # Ví dụ: from routes import main_bp; app.register_blueprint(main_bp)

    return app

# Đối tượng app dành cho Gunicorn (Render)
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)