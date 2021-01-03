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
    passwd = db.Column(db.String(300), nullable=True)
    is_activate = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), nullable=True, server_default=db.func.now())
    updated_at = db.Column(db.DateTime(), nullable=True, server_default=db.func.now(), onupdate=db.func.now())

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<User %r>' % self.username

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter_by(username=username).first()


class UserSchema(SQLAlchemySchema):

    class Meta:
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
        return hash_password(value)



