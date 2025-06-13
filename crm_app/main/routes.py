from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from . import main_bp
from ..forms import UpdateProfileForm # Import the new form
from ..extensions import db # Import db

@main_bp.route('/')
def home():
    return render_template('home.html', title='Home')

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm(original_username=current_user.username, original_email=current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
    return render_template('profile.html', title='Profile', form=form)
