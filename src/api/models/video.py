from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields


class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=True)
    image_url = db.Column(db.String(120), unique=True, nullable=True)
    video_url = db.Column(db.String(120), unique=True, nullable=True)
    description = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return '<Video %r>' % self.title


class VideoSchema(ModelSchema):

    class Meta(ModelSchema.Meta):
        model = Video
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    title = fields.String(required=True)
    image_url = fields.String(required=True)
    video_url = fields.String(required=True)
    description = fields.String(required=True)
