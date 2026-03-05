from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    balance = db.Column(db.BigInteger, default=0)
    is_active_account = db.Column(db.Boolean, default=True) # Mặc định là True (đang hoạt động)
    role = db.Column(db.String(10), default='user') # 'user' hoặc 'admin'
from datetime import datetime
from models import db

class Transaction(db.Model):
    __tablename__ = 'Transactions'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    amount = db.Column(db.BigInteger, nullable=False)
    content = db.Column(db.String(100)) # Nội dung khách ghi khi chuyển khoản
    status = db.Column(db.String(20), default='pending') # pending, success, canceled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Liên kết để lấy tên user dễ dàng
    user = db.relationship('User', backref=db.backref('transactions', lazy=True))