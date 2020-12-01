from datetime import datetime
from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class FileMixin:
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(120), unique=True, nullable=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<VideoFile %r>' % self.id

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class VideoFile(FileMixin, db.Model):

    _tablename_ = 'video_file'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))


class ImageFile(FileMixin, db.Model):

    _tablename_ = 'image_file'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

