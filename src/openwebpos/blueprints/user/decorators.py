from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user


def role_required(*roles):
    """
    Check if user has permission to view this page.

    param: *roles: 1 or more allowed roles
    return: Function
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.role not in roles:
                flash("You do not have permission.", "error")
                return redirect(url_for('pos.index'))
            return f(*args, **kwargs)

        return decorated_function

    return decorator
