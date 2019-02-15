import os

from flask import Flask, session, redirect, url_for, escape, request, render_template
from forms import LoginForm
from flask_wtf.csrf import CSRFProtect
from models import User
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

app = Flask(__name__)

app.secret_key = os.urandom(24)

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app=app)

# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# csrf protection
csrf = CSRFProtect()
csrf.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = User(user_name)
        if user.verify_password(password):
            login_user(user, remember=remember_me)
            return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', title="Sign In", form=form)

@app.route('/index')
def index():
    import pandas as pd
    df = pd.read_csv('./data/economic-indicators.csv', parse_dates=[['Year', 'Month']])
    length = len(df)
    return render_template('index.html', length=length,
                           dataframe=df.to_html())


if __name__ == '__main__':
    app.run(debug=True, port=5957)
