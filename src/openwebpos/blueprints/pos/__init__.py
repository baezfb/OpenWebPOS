from flask import Blueprint, render_template
from flask_login import login_required

from openwebpos.blueprints.user.decorators import staff_required
from .models import Category, Item, Option, Addon

bp = Blueprint('pos', __name__, template_folder='templates')


@bp.before_request
@login_required
@staff_required
def before_request():
    """
    Protects all the pos endpoints.
    """
    pass


@bp.get('/')
def index():
    categories = Category.query.filter_by(active=True).all()
    return render_template('pos/index.html', categories=categories)


@bp.get('/<category_items>')
def category(category_items):
    category_id = Category.query.filter_by(slug=category_items, active=True).first_or_404().id
    items = Item.query.filter_by(category_id=category_id, active=True).all()
    return render_template('pos/category.html', items=items)
