from flask import render_template, redirect, url_for, flash, request
from . import main
from .forms import LoginForm
from ..models import Student
from flask.ext.login import login_user, logout_user, login_required


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/login', methods=['GET', "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Student.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('students.view_students'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)


@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))
