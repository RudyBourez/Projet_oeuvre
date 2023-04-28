from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import check_password_hash
from .models import User
from flask_login import login_user, login_required, logout_user
auth = Blueprint('auth', __name__)

@auth.route('/connexion')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # On vérifie que le compte existe bien dans la base et que le mot de passe est correct
    if not user or not check_password_hash(user.password, password):
        flash('Assurez vous de renseigner une adresse et un mot de passe correct.', 'alert')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
    
    # On vérifie que le compte est actif
    if user.roles[0].is_active==1:
        login_user(user, remember=remember)
        flash(f'Vous êtes dorénavant connecté avec le compte suivant: {email}', 'success')
    else:
        flash('Votre compte est désactivé, contactez-nous pour le réactiver', 'alert')
        return redirect(url_for('auth.login'))
    return redirect(url_for('main.index'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))