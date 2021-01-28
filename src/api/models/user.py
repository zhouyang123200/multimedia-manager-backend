"""
user models and schema
"""
from flask import url_for, current_app
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
    avatar_image = db.Column(db.String(100), default=None)
    is_activate = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=True, server_default=func.now())
    updated_at = db.Column(db.DateTime(), nullable=True, server_default=func.now(),
     onupdate=func.now())

    def __repr__(self):
        return '<User %r>' % self.username

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
    avatar_image = fields.Method(serialize='get_image_url')
    is_activate = fields.Boolean()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    def load_passwd(self, value):
        """
        hash password when load
        """
        return hash_password(value)

    def get_image_url(self, user):
        """
        if user has avatar image, reuturn the url of image
        else return the url of default image
        """
        image_url = url_for('static', filename='assets/default-avatar.jpg')
        if user.avatar_image:
            image_url = url_for('static', filename='{}/avatars/{}'.format(user.name,
             user.avatar_image))
        return image_url
