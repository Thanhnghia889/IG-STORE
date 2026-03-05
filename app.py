import os
from flask import Flask, render_template
from extensions import db, login_manager # Import từ extensions
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    
    from config import Config
    app.config.from_object(Config)
    
    # Kết nối db và login_manager với app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        # Ép SQLite ghi dữ liệu ngay lập tức vào file .db
        try:
            db.session.execute(text('PRAGMA journal_mode=DELETE;'))
            db.session.execute(text('PRAGMA synchronous=FULL;'))
        except Exception:
            pass

        import models
        try:
            db.create_all()
            # Tạo admin mặc định
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
            print(">>> [HỆ THỐNG] Khởi tạo Database thành công!")
        except Exception as e:
            print(f">>> [LỖI] {e}")

    # Đăng ký Blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.route('/')
    def index():
        return render_template('index.html')

    return app

app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

if __name__ == "__main__":
    app.run(debug=True)