from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from .decorators import staff_required
from .forms import StaffLoginForm
from .models import User

user = Blueprint('user', __name__, template_folder='templates', url_prefix='/user/')


@user.before_request
def before_request():
    pass


@user.get('/login')
def login():
    """
    Login page.
    """
    # redirect to the index page if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pos.index'))
    form = StaffLoginForm()
    return render_template('user/login.html', form=form)


@user.post('/login')
def login_post():
    """
    Handle the POST request for the login form.
    """
    form = StaffLoginForm()
    if form.validate_on_submit():
        usr = User.query.filter_by(pin_id=form.pin.data).first()

        if usr and usr.is_active:
            login_user(usr)
            flash('You are logged in.', 'success')
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('pos.index')
                return redirect(next_page)
            return redirect(next_page)
    return redirect(url_for('user.login'))


@user.get('/logout')
@login_required
def logout():
    """
    Handle the logout request.
    """
    # Logout the user.
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('pos.index'))
