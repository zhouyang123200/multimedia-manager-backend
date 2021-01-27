"""
user models and schema
"""
from sqlalchemy import func
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow import fields
from api.utils.database import db, BaseMixin
from api.utils.passwd import hash_password


class User(BaseMixin, db.Model):
    """
    user model and some info
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    passwd = db.Column(db.String(300), nullable=True)
    is_activate = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=True, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=True, server_default=func.now(),
     onupdate=func.now())

    def __repr__(self):
        return '<User %r>' % self.username

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        """
        get user by username
        """
        return cls.query.filter_by(username=username).first()


class UserSchema(SQLAlchemySchema):
    """
    user model schema
    """

    class Meta:
        """
        meta class
        """
        model = User
        sqla_session = db.session
        load_instance = True

    id = fields.Integer(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    passwd = fields.Method(required=True, deserialize='load_passwd')
    is_activate = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def load_passwd(self, value):
        """
        hash password when dump
        """
        return hash_password(value)
