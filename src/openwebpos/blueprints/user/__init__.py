from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse

from .forms import StaffLoginForm
from .models import User, Role

bp = Blueprint('user', __name__, template_folder='templates', url_prefix='/user/')


@bp.get('/login')
def login():
    # redirect to the index page if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('pos.index'))
    form = StaffLoginForm()
    return render_template('user/login.html', form=form)


@bp.post('/login')
def login_post():
    form = StaffLoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(pin=form.pin.data).first_or_404()

        # check if the user exists
        if user is None:
            flash('Invalid pin')
            return redirect(url_for('user.login'))

        # Login the user if its active
        if login_user(user, remember=False) and user.is_active():
            user.update_activity_tracking(request.remote_addr)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('pos.index')
            flash('You are now logged in')
            return redirect(next_page)


@bp.get('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('pos.index'))
