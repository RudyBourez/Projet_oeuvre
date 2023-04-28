from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User, UserRoles
from flask_login import login_required
from flask_mail import Message
from .decorator import roles_required

from . import mail
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
    UserRoles.modify_user(email, role, is_active)
    flash('La base de donnée a correctement été modifiée', 'success')
    return redirect(url_for('admin.users'))

@admin.route('/creation', methods=['GET'])
@login_required
@roles_required("Admin")
def add_user():
    return render_template('add_users.html')

@admin.route('/creation', methods=['POST'])
@login_required
@roles_required("Admin")
def add_user_post():
    email=request.form.get('email')
    role=request.form.get('role')
    data = User.create_user(email, role)
    password = data[2]
    subject = "Création de votre compte pour l'application plafond de virements"
    msg = Message(subject, sender=email,recipients=[email])
    msg.body=f"Nous vous informons que votre compte a été crée:\n\nEmail: {email}\nMot de passe: {password}"
    mail.send(msg)
    flash(data[0], data[1])
    return redirect(url_for('admin.users'))