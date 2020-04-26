import sqlalchemy
from .db_session import SqlAlchemyBase


class Commands(SqlAlchemyBase):
    __tablename__ = 'commands'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    author = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    command_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    text = sqlalchemy.Column(sqlalchemy.String, default=None)
    img = sqlalchemy.Column(sqlalchemy.String, default=None)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

