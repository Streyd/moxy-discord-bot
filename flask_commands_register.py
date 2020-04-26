from flask import render_template, redirect, Blueprint
from data import db_session
from data.commands import Commands
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
from flask_login import login_required, current_user
import constants


command_register = Blueprint("command_register", __name__)


class CommandRegisterForm(FlaskForm):
    command_name = StringField('Calling of your command', validators=[DataRequired()])
    text = StringField('Text o your command')
    img = PasswordField('URL of your command\'s image or GIF')
    is_private = BooleanField("Private command")
    submit = SubmitField('Submit')


@command_register.route('/command_register', methods=['GET', 'POST'])
@login_required
def new_command():
    form = CommandRegisterForm()
    if form.validate_on_submit():
        if not form.text.data and not form.img.data:
            return render_template('command_register.html', title='New command',
                                   form=form,
                                   message="Text and image fields is empty. At least one field must be nor empty")
        if form.command_name.data[:8] == "https://" or form.command_name.data[:7] == "http://" or \
           form.text.data[:8] == "https://" or form.text.data[:7] == "http://":
            return render_template('command_register.html', title='New command',
                                   form=form,
                                   message="Command name and text can't be URL")
        session = db_session.create_session()
        if session.query(Commands).filter(Commands.command_name == form.command_name.data).first() or \
                form.command_name.data in constants.COMMANDS:
            return render_template('command_register.html', title='New command',
                                   form=form,
                                   message="Command name already exists")
        if form.img.data[:8] != "https://" and form.img.data[:7] != "http://":
            return render_template('command_register.html', title='New command',
                                   form=form,
                                   message="Image field must be URL")
        if form.command_name.data.count(" ") != 0:
            return render_template('command_register.html', title='New command',
                                   form=form,
                                   message="Command name must be without empty space between symbols")
        command = Commands(
                        author=current_user.id,
                        command_name=form.command_name.data,
                        text=form.text.data,
                        img=form.img.data,
                        is_private=form.is_private.data
                        )
        session.add(command)
        session.commit()
        return redirect('/login')
    return render_template('command_register.html', title='New command', form=form)

