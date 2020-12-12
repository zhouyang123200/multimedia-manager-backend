import os
from datetime import datetime
from flask import current_app
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow_sqlalchemy import fields as sqlma_fileds
from marshmallow import fields
from api.utils.database import db

class FileMixin:
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(120), unique=True, nullable=False)
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

    __tablename__ = 'video_file'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))


class ImageFile(FileMixin, db.Model):

    __tablename__ = 'image_file'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))


class VideoFileSchema(SQLAlchemySchema):

    class Meta:
        model = VideoFile
        load_instance = True
        sqla_session = db.session
    
    id = auto_field()
    created = auto_field()
    name = fields.String(required=True)
    file_path = fields.String(load_only=True)
    url = fields.Function(
        lambda obj: os.path.join(
            current_app.config['HOST'],
            current_app.config['STATIC_URL'],
            obj.file_path
        ))


class ImageFileSchema(SQLAlchemySchema):

    class Meta:
        model = ImageFile
        load_instance = True
        sqla_session = db.session
    
    id = auto_field()
    created = auto_field()
    name = fields.String(required=True)
    file_path = fields.String(load_only=True)
    url = fields.Function(
        lambda obj: os.path.join(
            current_app.config['HOST'],
            current_app.config['STATIC_URL'],
            obj.file_path
        ))