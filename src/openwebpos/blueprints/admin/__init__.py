import os

from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required
from slugify import slugify

from openwebpos.blueprints.pos.models import Category, Item, Option, Addon
from openwebpos.blueprints.user.decorators import admin_required
from openwebpos.utils import allowed_file, get_file_extension, delete_file
from .forms import CategoryForm, ItemForm

bp = Blueprint('admin', __name__, template_folder='templates', url_prefix='/admin')


@bp.before_request
@login_required
@admin_required
def before_request():
    """
    Protects all the admin endpoints.
    """
    pass


@bp.get('/')
def index():
    """
    Render the admin index page.
    """
    return redirect(url_for('admin.settings'))


@bp.get('/settings')
def settings():
    """
    Settings page.
    """
    return render_template('admin/settings.html')


@bp.get('/categories')
def categories():
    """
    List all categories.
    """
    category_form = CategoryForm()
    categories_list = Category.query.all()
    return render_template('admin/categories.html', categories_list=categories_list, category_form=category_form)


@bp.post('/add_category')
def add_category():
    """
    Add a category.
    """
    category_form = CategoryForm()
    if category_form.validate_on_submit():
        file = request.files['image']
        if file and allowed_file(file.filename):
            file_ext = get_file_extension(file.filename)
            filename = slugify(category_form.name.data) + '.' + file_ext
            file.save(os.path.join(os.getcwd(), 'uploads/', filename))
            category = Category(name=category_form.name.data, slug=None, description=category_form.description.data,
                                image=filename)
            category.save()
            flash('Category added successfully.', 'success')
        return redirect(url_for('admin.categories'))
    return redirect(url_for('admin.categories'))


@bp.get('/category/delete/<int:category_id>')
def delete_category(category_id):
    """
    Delete a category.
    """
    category = Category.query.get(category_id)
    if category and category.is_used() is False:
        category.delete()
        delete_file(current_app.config['UPLOAD_FOLDER'], category.image)
        flash('Category deleted successfully.', 'success')
    else:
        flash('Category not found.', 'danger')
        return redirect(url_for('admin.categories'))
    return redirect(url_for('admin.categories'))


@bp.get('/items')
def items():
    """
    List all items.
    """
    items_list = Item.query.all()
    available_categories = Category.query.filter_by(active=True).all()
    categories_list = [(category.id, category.name) for category in available_categories]
    item_form = ItemForm()
    item_form.categories.choices = categories_list
    options_list = Option.query.filter_by(active=True).all()
    addons_list = Addon.query.filter_by(active=True).all()
    return render_template('admin/items.html', items_list=items_list, item_form=item_form,
                           options_list=options_list, addons_list=addons_list)


@bp.post('/add_item')
def add_item():
    """
    Add an item.
    """
    available_categories = Category.query.filter_by(active=True).all()
    categories_list = [(category.id, category.name) for category in available_categories]
    item_form = ItemForm()
    item_form.categories.choices = categories_list
    if item_form.validate_on_submit():
        file = request.files['image']
        if file and allowed_file(file.filename):
            file_ext = get_file_extension(file.filename)
            filename = slugify(item_form.name.data) + '.' + file_ext
            file.save(os.path.join(os.getcwd(), 'uploads/', filename))
            item = Item(name=item_form.name.data, description=item_form.description.data,
                        image=filename, price=item_form.price.data, category_id=item_form.categories.data)
            item.save()
            flash('Item added successfully.', 'success')
        return redirect(url_for('admin.items'))
    return redirect(url_for('admin.items'))


@bp.get('/item/delete/<int:item_id>')
def delete_item(item_id):
    """
    Delete an item.
    """
    item = Item.query.get(item_id)
    if item.is_used():
        flash('Item is used and cannot be deleted.', 'danger')
        return redirect(url_for('admin.items'))
    if item:
        item.delete()
        delete_file(current_app.config['UPLOAD_FOLDER'], item.image)
        flash('Item deleted successfully.', 'success')
    else:
        flash('Item not found.', 'danger')
        return redirect(url_for('admin.items'))
    return redirect(url_for('admin.items'))
