from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow import fields
from .file import VideoFileSchema

class Video(db.Model):

    _tablename_ = 'video'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=True)
    video_files = db.relationship('VideoFile', backref='video', lazy=False)
    image_files = db.relationship('ImageFile', backref='video', lazy=False)
    description = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Video %r>' % self.title

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class VideoSchema(ModelSchema):

    class Meta(ModelSchema.Meta):
        model = Video
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    video = Nested(VideoFileSchema, many=True, exclude=("video",))
    description = fields.String(required=True)
