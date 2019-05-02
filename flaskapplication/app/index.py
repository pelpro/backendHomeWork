from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm
from flask_login import current_user, login_user
from app.models import User
from flask_login import logout_user
from flask_login import login_required
from flask import request, url_for
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app import db
import datetime
from itsdangerous import URLSafeTimedSerializer



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'nickname': 'Andrew'}
    posts = [  # список выдуманных постов
        {
            'author': {'nickname': 'Man'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'John'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template("index.html",
                           title='Home',
                           posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/confirm/<token>')
@login_required
def confirm_email():
    form = MailForm()
    if form.validate_on_submit():
        token = serializer.dumps(form.email.data)
        user = User.query.filter_by(email=form.email.data).first()
        user.token = token
        db.session.commit()
        send_confirmation(form.email.data, token)
        return render_template('activate.html',
                               text='Confirmation message send.',
                               form=form,
                               failed=True)

    cur_token = request.args.get('token', '')
    if cur_token == '':
        return render_template('activate.html', text='Resend confirmation message', form=form, failed=True)
    user = User.query.filter_by(token=cur_token).first()
    try:
        cur_mail = serializer.loads(user.token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration)
        user.confirmed = True
        db.session.commit()
    except:
        return false
    return redirect(url_for('login'))
