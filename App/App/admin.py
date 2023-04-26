from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User, UserRoles
from flask_login import login_required, current_user
from .decorator import roles_required

admin =  Blueprint("admin", __name__)

@admin.route('/utilisateurs')
@login_required
@roles_required("Admin")
def users():
    data = User.get_all_user()
    return render_template("users.html", data=data)

@admin.route('/update', methods=['GET'])
@login_required
@roles_required("Admin")
def modify_users():
    id = int(request.args.get("id"))
    data = User.get_user_by_id(id)
    return render_template("modify_users.html", data=data)

@admin.route('/update', methods=['POST'])
@login_required
@roles_required("Admin")
def modify_users_post():
    email = request.form.get('email')
    role = request.form.get('role')
    is_active = int(request.form.get('is_active'))
    data = UserRoles.modify_user(email, role, is_active)
    flash('La base de donnée a correctement été modifiée', 'success')
    return redirect(url_for('admin.users'))