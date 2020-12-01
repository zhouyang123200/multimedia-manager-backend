
from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class File(db.Model):

    _tablename_ = 'file'

    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(120), unique=True, nullable=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<File %r>' % self.title

    def delete(self):
        db.session.delete(self)
        db.session.commit()