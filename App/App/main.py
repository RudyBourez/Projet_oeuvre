from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_mail import Message
from flask_login import login_required
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