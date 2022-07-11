from flask import Blueprint, render_template
from flask_login import login_required

from openwebpos.blueprints.user.decorators import role_required

bp = Blueprint('pos', __name__, template_folder='templates')


@bp.before_request
@login_required
@role_required('admin, staff')
def before_request():
    """
    Protects all the pos endpoints.
    """
    pass


@bp.get('/')
def index():
    return render_template('pos/index.html')
