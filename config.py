import os

# Xác định đường dẫn thư mục hiện tại
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Mã bí mật để bảo mật Session/Cookie
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'igstore_secret_key_123'
    
    # Cấu hình đường dẫn file database.db ngay tại thư mục gốc
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')
    
    # Tắt tính năng theo dõi thay đổi để tiết kiệm RAM
    SQLALCHEMY_TRACK_MODIFICATIONS = False