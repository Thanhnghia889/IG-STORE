from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User

admin_bp = Blueprint('admin', __name__)

# Hàm kiểm tra quyền admin
def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'
@admin_bp.route('/admin/dashboard')
@login_required
def dashboard():
    if not is_admin():
        return "Bạn không có quyền!", 403
    users = User.query.all()
    return render_template('admin.html', users=users)

@admin_bp.route('/admin/add-money', methods=['POST'])
@login_required
def add_money():
    if not is_admin():
        return "Không có quyền!", 403
    
    user_id = request.form.get('user_id')
    amount = int(request.form.get('amount'))
    
    user = User.query.get(user_id)
    if user:
        user.balance += amount
        db.session.commit()
        print(f"Đã cộng {amount} cho user {user.username}")
    
    return redirect(url_for('admin.dashboard'))
@admin_bp.route('/admin/toggle-ban/<int:user_id>', methods=['POST'])
def toggle_ban(user_id):
    if not is_admin():
        return "Không có quyền!", 403
    
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        return "Bạn không thể tự khóa chính mình!", 400

    # Đảo ngược trạng thái: True -> False, False -> True
    user.is_active_account = not user.is_active_account
    db.session.commit()
    
    status = "Khóa" if not user.is_active_account else "Mở khóa"
    print(f"Admin đã {status} tài khoản {user.username}")
    
    return redirect(url_for('admin.dashboard'))
@admin_bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not is_admin():
        return "No Access", 403
        
    user_to_delete = User.query.get(user_id)
    
    if user_to_delete:
        # Kiểm tra không cho admin tự xóa chính mình
        if user_to_delete.id == current_user.id:
            print("DEBUG: Khong the tu xoa chinh minh!")
            return redirect(url_for('admin.dashboard'))

        try:
            db.session.delete(user_to_delete)
            db.session.commit() # Lưu thay đổi vào SQL Server
            print(f"DEBUG: Da xoa thanh cong User ID {user_id}")
        except Exception as e:
            db.session.rollback() # Nếu lỗi thì quay lại trạng thái cũ
            print(f"DEBUG: Loi khi xoa: {str(e)}")
            
    return redirect(url_for('admin.dashboard'))