from app import db, app
from app.models import User, Role
from datetime import date
from werkzeug.security import generate_password_hash

app.app_context().push()
db.create_all()


if not User.query.filter(User.email == 'admin@example.com').first():
    admin = User(
        email='admin@example.com',
        password=generate_password_hash('1234'),
        date_inscription=date(2023,4,25)
    )

if not User.query.filter(User.email == 'admin1@example.com').first():
    admin1 = User(
        email='admin1@example.com',
        password=generate_password_hash('1234'),
        date_inscription=date(2023,4,25)
    )


if not User.query.filter(User.email == 'user@example.com').first():       
    user = User(
        email="user@example.com",
        password=generate_password_hash('123456'),
        date_inscription=date(2023,4,25)
    )
    
if not User.query.filter(User.email == 'user1@example.com').first():       
    user1 = User(
        email="user1@example.com",
        password=generate_password_hash('123456'),
        date_inscription=date(2023,4,25)
    )
        
if not User.query.filter(User.email == 'director@example.com').first():       
    director = User(
        email="director@example.com",
        password=generate_password_hash('123456'),
        date_inscription=date(2023,4,25)
    )
if not User.query.filter(User.email == 'director1@example.com').first():       
    director1 = User(
        email="director1@example.com",
        password=generate_password_hash('123456'),
        date_inscription=date(2023,4,25)
    )

admin_role = Role(name="Admin", is_active=1)
admin_role1 = Role(name="Admin", is_active=0)
supervisor_role = Role(name="Supervisor", is_active=1)
supervisor_role1 = Role(name="Supervisor", is_active=0)
user_role = Role(name="User", is_active=1)
user_role1 = Role(name="User", is_active=0)

director.roles.append(supervisor_role)
director1.roles.append(supervisor_role1)
user.roles.append(user_role)
user1.roles.append(user_role1)
admin.roles.append(admin_role)
admin1.roles.append(admin_role1)

db.session.add(director)    
db.session.add(director1)    
db.session.add(admin)
db.session.add(admin1)
db.session.add(user)
db.session.add(user1)
db.session.commit()