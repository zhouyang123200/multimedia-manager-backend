from flask import Blueprint, request
from flask_restful import Api, Resource
from api.models.video import VideoSchema, Video

video_route = Blueprint('video_route', __name__)
video_api = Api(video_route)


class VideoItem(Resource):

    def get(self, id):
        return {'video': 'a video'}


class VideoList(Resource):

    def get(self):
        video_schema = VideoSchema()
        videos = Video.query.all()
        print(videos)
        result = video_schema.dumps(videos, many=True)
        return result, 200

    def post(self):
        data = request.get_json()
        video_schema = VideoSchema()
        video = video_schema.load(data)
        result = video_schema.dump(video.save())
        return result, 201


video_api.add_resource(VideoItem, '/video/<int:id>')
video_api.add_resource(VideoList, '/videos')
