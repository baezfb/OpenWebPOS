from collections import OrderedDict
from datetime import datetime

from flask_login import UserMixin
from usernames import is_safe_username
from werkzeug.security import generate_password_hash, check_password_hash

from openwebpos.extensions import db
from openwebpos.utils import gen_urlsafe_token
from openwebpos.utils.sql import SQLMixin


class User(UserMixin, SQLMixin, db.Model):
    ROLE = OrderedDict([
        ('customer', 'Customer'),
        ('staff', 'Staff'),
        ('admin', 'Admin')
    ])

    __tablename__ = "user"

    public_id = db.Column(db.String(100), unique=True)

    # Authentication
    role = db.Column(db.Enum(*ROLE, name='role_types', native_enum=False), index=True, nullable=False,
                     server_default='customer')
    username = db.Column(db.String(120), unique=True, index=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(120), nullable=False, server_default='')
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='1')

    # Activity tracking
    sign_in_count = db.Column(db.Integer, nullable=False, default=0)
    current_sign_in_at = db.Column(db.DateTime, nullable=True)
    current_sign_in_ip = db.Column(db.String(100), nullable=True)
    last_sign_in_at = db.Column(db.DateTime, nullable=True)
    last_sign_in_ip = db.Column(db.String(100), nullable=True)

    def check_password(self, password):
        return check_password_hash(password, self.password)

    def is_active(self):
        """
        Return whether user account is active.
        :return: bool
        """
        return self.active

    def update_activity_tracking(self, ip_address: str):
        """
        Update the fields associated with user activity tracking.
        ip_address: str, IP address of the user.
        """
        self.last_sign_in_at = self.current_sign_in_at
        self.last_sign_in_ip = self.current_sign_in_ip
        self.current_sign_in_at = datetime.utcnow()
        self.current_sign_in_ip = ip_address
        self.sign_in_count += 1

        return self.save()

    def __init__(self, username, email, password):
        self.username = is_safe_username(username)
        self.email = email
        self.password = generate_password_hash(password)
        self.public_id = gen_urlsafe_token(100)
