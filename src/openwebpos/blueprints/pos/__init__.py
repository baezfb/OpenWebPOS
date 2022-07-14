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

    # insert categories to the database if none are present
    if not Category.query.first():
        Category.insert_categories()

    if not Item.query.first():
        Item.insert_items()

    if not Option.query.first():
        Option.insert_options()

    if not Addon.query.first():
        Addon.insert_addons()


@bp.get('/')
def index():
    categories = Category.query.filter_by(active=True).all()
    return render_template('pos/index.html', categories=categories)


@bp.get('/<category_items>')
def category(category_items):
    category_id = Category.query.filter_by(slug=category_items, active=True).first_or_404().id
    items = Item.query.filter_by(category_id=category_id, active=True).all()
    return render_template('pos/category.html', items=items)
