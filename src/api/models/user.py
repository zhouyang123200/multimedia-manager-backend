from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy import fields as sqlma_fields
from marshmallow import fields, Schema, validates, ValidationError
from api.utils.database import db
from api.utils.passwd import hash_password


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120), unique=True)
    passwd = db.Column(db.String(300))
    is_activate = db.Column(db.Boolean(), default=False)
    createed = db.Column(db.DateTime(), nullable=True, server_default=db.func.now())
    updated = db.Column(db.DateTime(), nullable=True, server_default=db.func.now(), onupdated=db.fun.now())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.title

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username),first()


class UserSchema(SQLAlchemySchema):

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    passwd = fields.String(required=True, deserialize='load_passwd')
    is_activate = fields.Boolean()
    created = fields.DateTime()
    updated = fields.DateTime()

    def load_passwd(self, value):
        return hash_password(value)



