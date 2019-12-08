from api.utils.database import db


class Video(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.string(120), unique=True, nullable=True)
    image_url = db.Column(db.string(120), unique=True, nullable=True)
    video_url = db.Column(db.string(120), unique=True, nullable=True)
    description = db.Column(db.string(120))

    def __repr__(self):
        return '<Video %r>' % self.title
