from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from flask_mail import Message
from .models import User
from werkzeug.security import check_password_hash
from flask_login import login_required, current_user
from .decorator import roles_required
from . import mail
import os

main =  Blueprint("main", __name__)

@main.route('/')
@main.route('/accueil')
@login_required
def index():
    return render_template("index.html")

@main.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@main.route('/contact', methods=['POST'])
def contact_post():
    email=request.form.get('email')
    subject=request.form.get('subject')
    comment=request.form.get('comment')
    msg = Message(subject, sender=email,recipients=['bourez.rudy@gmail.com'])
    msg.body=f" Email utilisateur: {email}\n\n{comment}"
    mail.send(msg)
    flash('Votre message a été envoyé avec succès.', "success")
    return redirect(url_for("auth.login"))

@main.route('/clients')
@login_required
def clients():
    return render_template('clients.html')

@main.route('/plafonds')
@login_required
def plafonds():
    return render_template('plafonds.html')

@main.route('/suivi')
@login_required
@roles_required("Supervisor")
def suivi():
    return render_template('suivi.html')

@main.route('/update_password', methods=['GET'])
@login_required
def update_password():
    return render_template('update_password.html')

@main.route('/update_password', methods=['POST'])
@login_required
def update_password_post():
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    if password == confirm_password:
        User.modify_password(current_user.email, password)
        flash('Votre mot de passe a été changé.', "success")
        return redirect(url_for('main.index'))
    flash('Les deux mots de passe ne sont pas identiques', 'alert')
    return redirect(url_for('main.update_password'))