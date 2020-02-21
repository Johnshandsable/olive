from flask import Blueprint, render_template, url_for, redirect, request, current_app, flash
from flask_login import current_user, login_user, login_required
from app import bcrypt
from app.models import User, UserLogin
from app.users.forms import LoginForm, RegistrationForm, UserSearch

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = UserLogin(username=form.username.data, password=hashed_password)
        user.add_login(user)
        flash('Your account has been created!', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login = LoginForm()
    if login.validate_on_submit():
        user_login = UserLogin.query.filter_by(username=login.username.data).first()
        if user_login and bcrypt.check_password_hash(user_login.password, login.password.data):
            login_user(user_login, remember=login.remember.data)
            return redirect(url_for('main.index'))
        else:
            flash('Login unsuccessful', 'danger')
    return render_template("login.html", login=login)


@users.route("/search", methods=['GET', 'POST'])
@login_required
def search():
    user_search_form = UserSearch()
    if user_search_form.validate_on_submit() and request.method == 'POST':
        user_search_query = User.query.filter_by(family_name=user_search_form.family_name.data, family_size=user_search_form.family_size.data).all()
        return render_template("search.html", search_form=user_search_form, user_search_query=user_search_query)
    else:
        return render_template("search.html", search_form=user_search_form)
