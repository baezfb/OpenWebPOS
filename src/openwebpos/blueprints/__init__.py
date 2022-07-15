from .admin import bp as admin_bp
from .pos import bp as pos_bp
from .user import bp as user_bp

blueprints = [
    user_bp,
    pos_bp,
    admin_bp
]
