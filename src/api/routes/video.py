import os
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from api.models.video import VideoSchema, Video

video_route = Blueprint('video_route', __name__)
video_api = Api(video_route)


class VideoItem(Resource):

    video_schema = VideoSchema()

    def get(self, id):
        video = Video.query.get(id)
        result = self.video_schema.dump(video)
        return result, 200

    def put(self, id):
        video = Video.query.get(id)
        for key, value in video.items():
            setattr(video, key, value)
        video.save()
        result = self.video_schema.dump(video)
        return result, 200

    def delete(self, id):
        video = Video.query.get(id)
        if video:
            video.delete()
        return {}, 204


class VideoList(Resource):

    video_schema = VideoSchema()

    def get(self):
        videos = Video.query.all()
        result = self.video_schema.dumps(videos, many=True)
        return result, 200

    def post(self):
        data = request.get_json()
        video = self.video_schema.load(data)
        result = self.video_schema.dump(video.save())
        return result, 201


class UploadFiles(Resource):

    def post(self):
        file = request.files['upload_file']
        file.save(
            os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))
        return {'upload_file': file.filename}, 200


video_api.add_resource(VideoItem, '/video/<int:id>')
video_api.add_resource(VideoList, '/videos')
video_api.add_resource(UploadFiles, '/files')
