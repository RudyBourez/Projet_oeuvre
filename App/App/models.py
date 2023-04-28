from flask_login import UserMixin
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from . import db
from datetime import date
from .password_generator import generate_password

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    date_inscription = db.Column(db.Date)
    roles = db.relationship('Role', secondary='UserRole',
            backref=db.backref('users', lazy='dynamic'))
    
    @classmethod
    def get_all_user(cls):
        conn = db.session()
        cursor = conn.execute(text('''
                                    SELECT USERS.EMAIL, USERS.DATE_INSCRIPTION, ROLES.NAME, ROLES.IS_ACTIVE, USERS.ID
                                    FROM User USERS
                                    LEFT JOIN USERROLE USERROLES ON USERS.ID=USERROLES.USER_ID
                                    LEFT JOIN ROLE ROLES ON ROLES.ID=USERROLES.ROLE_ID
                                    ''')).cursor
        return cursor.fetchall()
    
    @classmethod
    def create_user(cls, email, role):
        conn = db.session()
        user = conn.execute(text(f'SELECT * FROM USER WHERE EMAIL="{email}"')).cursor.fetchone()
        if not user:
            # On crée le role pour l'attacher à l'utilisateur
            relation = Role(name=role, is_active=1)
            # On crée le nouvel utilisateur avec son role attaché et un mot de passe aléatoire
            password = generate_password(16)
            user = User(email=email, password=generate_password_hash(password),date_inscription=date.today())
            # On attache le role à l'utilisateur
            user.roles.append(relation)
            db.session.add(user)
            db.session.commit()
            return [f"Le compte a bien été crée\n{email}: Role {role}", "success", password]
        else:
            return ["Cette adresse mail est déjà utilisée", "alert"]
    
    @classmethod
    def get_user_by_id(cls, id):
        conn = db.session()
        cursor = conn.execute(text(f'''
                                    SELECT USERS.EMAIL, USERS.DATE_INSCRIPTION, ROLES.NAME, ROLES.IS_ACTIVE
                                    FROM User USERS
                                    LEFT JOIN USERROLE USERROLES ON USERS.ID=USERROLES.USER_ID
                                    LEFT JOIN ROLE ROLES ON ROLES.ID=USERROLES.ROLE_ID
                                    WHERE USERS.ID={id}
                                    ''')).cursor
        return cursor.fetchone()
    
    @classmethod
    def modify_password(cls, email, password):    
        conn = db.session()
        conn.execute(text(f'UPDATE USER SET PASSWORD="{generate_password_hash(password)}" WHERE EMAIL="{email}"'))
        db.session.commit()
        return "Votre compte a bien été crée"
    
# Définition du modèle gérant les Roles
class Role(db.Model):
    __tablename__ = 'Role'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50))
    is_active = db.Column(db.Integer())
    
    @classmethod
    def get_role_id(cls, name, is_active):
        conn = db.session()
        cursor = conn.execute(text(f'SELECT ID FROM ROLE WHERE NAME="{name}" AND IS_ACTIVE={is_active}')).cursor
        return cursor.fetchone()[0]
    
# Define UserRoles model
class UserRoles(db.Model):
    __tablename__ = 'UserRole'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('Role.id', ondelete='CASCADE'))
    
    @classmethod
    def modify_user(cls, email, role, is_active):
        conn = db.session()
        # On récupére l'id de l'utilisateur
        id = conn.execute(text(f'SELECT ID FROM USER WHERE EMAIL="{email}"')).cursor.fetchone()[0]
        # On récupére le nouvel id du role
        role_id = Role.get_role_id(role, is_active)
        # On modifie l'entrèe
        conn.execute(text(f'''
                          UPDATE USERROLE
                          SET ROLE_ID={role_id}
                          WHERE USERROLE.USER_ID={id}
                     '''))
        db.session.commit()
        return "Modification correctement effectuée"