import os
import json
import shutil
import time
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from api.models import VideoSchema, Video

video_route = Blueprint('video_route', __name__)
video_api = Api(video_route)


class VideoItem(Resource):

    video_schema = VideoSchema()
    static_url = '/static/'
    media_url = '/media/'

    def get(self, id):
        video = Video.query.get(id)
        result = self.video_schema.dump(video)
        return result, 200

    def put(self, id):
        video = Video.query.get(id)
        data = request.get_json()
        for key, value in video.items():
            if key in data:
                setattr(video, key, data.get(key))
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
        video_data = self.convert_timestamp_info(data)
        video = self.video_schema.load(video_data)
        ret = self.video_schema.dump(video.save())
        return ret, 201

    @staticmethod
    def convert_timestamp_info(data):
        videos = data.get('videos')
        images = data.get('images')

        # judge the exits of video and images
        upload_path = current_app.config['UPLOAD_FOLDER']
        storage_path = current_app.config['FILE_STORAGE_PATH']
        title = data.get('title')
        storage_dir = os.path.join(storage_path, title)

        for video in videos:
            video_num = video.get('video_num')
            video_name = video.get('video_name')
            video_upload_path = os.path.join(upload_path, video_num)
            video_storage_path = os.path.join(storage_dir, video_name)      
            shutil.move(video_upload_path, video_storage_path)
            video['file_path'] = os.path.join(title, video_name)
            del video['video_num']

        for image in images:
            image_num = image.get('image_num')
            image_name = image.get('image_name')
            image_upload_path = os.path.join(upload_path, image_num)
            image_storage_path = os.path.join(storage_dir, image_name)
            shutil.move(image_upload_path, image_storage_path)
            image['file_path'] = os.path.join(title, image_name)
            del image['image_num']

        return ret


class UploadFiles(Resource):

    def post(self):
        filename = str(time.time())
        filepath = os.path.join(
            os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        with open(filepath, 'bw') as f:
            chunk_size = 1024
            while True:
                chunk = request.stream.read(chunk_size)
                if len(chunk) == 0:
                    break
                f.write(chunk)
        print(filename)
        return {'timestamp': filename}, 200


video_api.add_resource(VideoItem, '/api/video/<int:id>')
video_api.add_resource(VideoList, '/api/videos')
video_api.add_resource(UploadFiles, '/api/files')
