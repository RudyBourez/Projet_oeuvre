from flask_login import UserMixin
from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from . import db
from datetime import date

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
    def create_user(cls, email):
        conn = db.session()
        conn.execute(text(f'INSERT INTO USER VALUES ("{email}", "{generate_password_hash("this_is_the_first_password")}", {date.today()})'))
        db.session.commit()
        cursor = conn.execute(text(f'SELECT MAX(ID) FROM USER'))
        return cursor.fetchone()
    
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
    
# Define Role model
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
        role_id = conn.execute(text(f'SELECT ID FROM ROLE WHERE NAME="{role}" AND IS_ACTIVE={is_active}')).cursor.fetchone()[0]
        # On modifie l'entrèe
        conn.execute(text(f'''
                          UPDATE USERROLE
                          SET ROLE_ID={role_id}
                          WHERE USERROLE.USER_ID={id}
                     '''))
        db.session.commit()
        return "Modification correctement effectuée"
    
    @classmethod
    def attach_role(cls, user_id, role_id):
        conn = db.session()
        conn.execute(text(f'INSERT INTO USERROLE VALUES ({user_id}, {role_id})'))
        return 'Le compte a bien été crée'