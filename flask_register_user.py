from flask import render_template, redirect, Blueprint
from data import db_session
from data.users import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


user_register = Blueprint("user_register", __name__)


class RegisterForm(FlaskForm):
    discord_id = StringField('Discord user id (example#1234)', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Let\'s Go')


@user_register.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Password mismatch")
        if form.discord_id.data.count("#") != 1:
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Discord ID doesn't match with pattern ")
        if len(form.discord_id.data.split("#")[1]) != 4 or not form.discord_id.data.split("#")[1].isdigit():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Discord ID doesn't match with pattern ")
        session = db_session.create_session()
        if session.query(User).filter(User.discord_id == form.discord_id.data).first():
            return render_template('register.html', title='Registration',
                                   form=form,
                                   message="Discord ID already registered")
        user = User(discord_id=form.discord_id.data)
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Registration', form=form)


