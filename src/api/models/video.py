"""
video models and schema
"""
from sqlalchemy import func
from marshmallow_sqlalchemy import SQLAlchemySchema
from marshmallow_sqlalchemy import fields as sqlma_fields
from marshmallow import fields, Schema, validates, ValidationError

from api.utils.database import db
from api.utils.paginator import PaginationSchema
from .file import VideoFileSchema, ImageFileSchema

class Video(db.Model):
    """
    video model
    """

    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=True)
    video_files = db.relationship('VideoFile', backref=db.backref('video'), lazy=False)
    image_files = db.relationship('ImageFile', backref=db.backref('video'), lazy=False)
    created_at = db.Column(db.DateTime(), nullable=True, server_default=func.now())
    description = db.Column(db.String(120))

    def save(self):
        """
        item save methed
        """
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Video %r>' % self.title

    def delete(self):
        """
        object delete methed
        """
        db.session.delete(self)
        db.session.commit()


class VideoSchema(SQLAlchemySchema):
    """
    video schema
    """

    class Meta:
        """
        meta class
        """
        model = Video
        sqla_session = db.session
        load_instance = True

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    video_files = sqlma_fields.Nested(VideoFileSchema, many=True, exclude=("id", "created"))
    image_files = sqlma_fields.Nested(ImageFileSchema, many=True, exclude=("id", "created"))
    created_at = fields.DateTime(dump_only=True)
    description = fields.String(required=True)


class VideoPaginationSchema(PaginationSchema):
    """
    video schema for pagination
    """
    data = fields.Nested(VideoSchema, attribute='items', many=True)


class RawFileSchema(Schema):
    """
    raw upload file schema
    """

    name = fields.String()
    num = fields.String()

    @validates('num')
    def verify_timestamp(self, value):
        """
        verify the file is the required format
        """
        if len(value) != 18 or value[10] != '.':
            raise ValidationError('This is not a timestamp!')

class VideoRawSchema(Schema):
    """
    video raw schema
    """

    title = fields.String(required=True)
    video_files = fields.List(fields.Nested(RawFileSchema))
    image_files = fields.List(fields.Nested(RawFileSchema))
    description = fields.String()
