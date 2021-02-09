"""
all kinds of file model and related schema
"""
import os
from datetime import datetime
from flask import current_app
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields
from api.utils.database import db, BaseMixin

class FileMixin:
    """
    base model for file
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(120), unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class VideoFile(FileMixin, BaseMixin, db.Model):
    """
    video file model
    """

    __tablename__ = 'video_file'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

    def __repr__(self):
        return '<VidelFile %r>' % self.id

    def delete(self):
        """
        delete this entry and related file
        """
        os.remove(self.file_path)
        super(VideoFile, self).delete()


class ImageFile(FileMixin, BaseMixin, db.Model):
    """
    image file model
    """

    __tablename__ = 'image_file'

    video_id = db.Column(db.Integer, db.ForeignKey('video.id'))

    def __repr__(self):
        return '<ImageFile %r>' % self.id

class VideoFileSchema(SQLAlchemySchema):
    """
    video file model schema
    """

    class Meta:
        """
        meta class
        """
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
    """
    image file model schema
    """

    class Meta:
        """
        meta class
        """
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
