from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db 
from models import User

admin_bp = Blueprint('admin', __name__)

# Hàm kiểm tra quyền admin
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not is_admin():
        flash("Bạn không có quyền truy cập trang này!", "danger")
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin.html', users=users)

@admin_bp.route('/admin/add-money', methods=['POST'])
@login_required
def add_money():
    if not is_admin(): 
        return "Không có quyền!", 403
        
    user_id = request.form.get('user_id')
    amount_str = request.form.get('amount')
    
    if not amount_str or not amount_str.isdigit():
        flash("Số tiền không hợp lệ!", "warning")
        return redirect(url_for('admin.dashboard'))
        
    amount = int(amount_str)
    user = User.query.get(user_id)
    
    if user:
        user.balance += amount
        db.session.commit()
        flash(f"Đã cộng {amount:,}đ cho tài khoản {user.username}", "success")
    else:
        flash("Không tìm thấy người dùng!", "danger")
        
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/toggle-ban/<int:user_id>', methods=['POST'])
@login_required
def toggle_ban(user_id):
    if not is_admin(): 
        return "Không có quyền!", 403
        
    user = User.query.get_or_404(user_id)
    
    # Không cho phép admin tự khóa chính mình
    if user.id == current_user.id:
        flash("Bạn không thể tự khóa tài khoản của chính mình!", "danger")
        return redirect(url_for('admin.dashboard'))
        
    user.is_active_account = not user.is_active_account
    db.session.commit()
    
    trang_thai = "Mở khóa" if user.is_active_account else "Khóa"
    flash(f"Đã {trang_thai} tài khoản {user.username} thành công!", "info")
    
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not is_admin(): 
        return "Không có quyền!", 403
        
    user = User.query.get(user_id)
    if user:
        if user.id == current_user.id:
            flash("Không thể xóa chính mình!", "danger")
        else:
            db.session.delete(user)
            db.session.commit()
            flash(f"Đã xóa vĩnh viễn người dùng {user.username}!", "success")
            
    return redirect(url_for('admin.dashboard'))