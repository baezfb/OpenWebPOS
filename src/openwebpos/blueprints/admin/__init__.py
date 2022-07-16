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
