from flask import render_template
from flask_login import current_user, LoginManager
from flask_wtf import FlaskForm
from wtforms import SubmitField
from flask import Flask
from flask_register_user import user_register
from flask_login_user import user_login
from flask_commands_register import command_register
from data.users import User
import data.db_session as db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'discord_super_puper_duper_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
app.register_blueprint(user_register)
app.register_blueprint(user_login)
app.register_blueprint(command_register)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


class NotLoginStartPageForm(FlaskForm):
    login = SubmitField('Login')
    register = SubmitField('Register')


class LoginStartPageForm(FlaskForm):
    my_commands = SubmitField('My Commands')
    add_command = SubmitField('Add new command')
    command_workshop = SubmitField('All public commands')
    logout = SubmitField('Logout')


@app.route('/', methods=['GET', 'POST'])
def start_page():
    if current_user:
        form = LoginStartPageForm
    else:
        form = NotLoginStartPageForm
    return render_template('start_page.html', title='Moxy', form=form)


db_session.global_init(
                        user="tgzxcghuodsobc",
                        password="bac16d06b380d43e040d01b3aba7bdeb92c9c5ad904d69fce184504252ac79cb",
                        hostname="ec2-54-228-209-117.eu-west-1.compute.amazonaws.com",
                        port="5432",
                        database_name="d960kjpc5g6169"
                       )





