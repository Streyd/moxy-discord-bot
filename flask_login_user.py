from flask_login import login_user, login_required, logout_user
import data.db_session as db_session
from data.users import User
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired
from flask import redirect, render_template, Blueprint


user_login = Blueprint("user_login", __name__)


class LoginForm(FlaskForm):
    discord_id = StringField('Discord ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Submit')


@user_login.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.discord_id == form.discord_id.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/command_register")
        return render_template('login.html',
                               message="Wrong Discord ID or Password",
                               form=form)
    return render_template('login.html', title='Login', form=form)


@user_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")
