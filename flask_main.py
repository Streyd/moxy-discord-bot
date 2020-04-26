from flask import Flask
from flask_login import LoginManager
import data.db_session as db_session
from flask_register_user import user_register
from flask_commands_register import command_register
from flask_login_user import user_login
from data.users import User

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


def main():
    print(1)
    db_session.global_init("data/db/custom_commands.sqlite")
    app.run()


if __name__ == '__main__':
    main()
