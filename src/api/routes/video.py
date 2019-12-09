from flask import Blueprint
from flask_restful import Api, Resource


video_route = Blueprint('video_route', __name__)
video_api = Api(video_route)


class VideoItem(Resource):

    def get(self, id):
        return {'video': 'a video'}


class VideoList(Resource):

    def get(self):
        return {'videos': 'video list'}


video_api.add_resource(VideoItem, '/video/<int:id>')
video_api.add_resource(VideoList, '/videos')
