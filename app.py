from flask import Flask, render_template
from config import Config
from models import db
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo Database
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Nó sẽ tự kiểm tra, nếu chưa có bảng thì nó tự tạo
    return app

    # Cấu hình Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))

    # --- ĐĂNG KÝ BLUEPRINT PHẢI NẰM TRONG HÀM NÀY ---
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    # Route trang chủ
    @app.route('/')
    def index():
        return render_template('index.html')

    # Route nạp tiền
    @app.route('/recharge')
    def recharge():
        return render_template('recharge.html')

    return app

# Khởi chạy ứng dụng
if __name__ == '__main__':
    app = create_app() # Biến app được tạo ra ở đây
    with app.app_context():
        db.create_all()
    app.run(debug=True)