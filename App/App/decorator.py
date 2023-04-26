from functools import wraps
from flask import abort
from flask_login import current_user


def roles_required(role):
    """Restrict a view to users with the given permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.roles[0].name != role:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
        
    