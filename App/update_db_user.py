from app import db, app
from app.models import User, Role
from datetime import date
from werkzeug.security import generate_password_hash

app.app_context().push()
db.create_all()