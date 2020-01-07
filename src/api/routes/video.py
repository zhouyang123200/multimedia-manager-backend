import os
import json
import shutil
import time
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from api.models.video import VideoSchema, Video

video_route = Blueprint('video_route', __name__)
video_api = Api(video_route)


class VideoItem(Resource):

    video_schema = VideoSchema()
    static_url = '/static/'
    media_url = '/media/'

    def get(self, id):
        video = Video.query.get(id)
        result = self.video_schema.dump(video)
        image_filename = os.path.basename(result['image_url'])
        image_url = os.path.join(self.static_url, image_filename)
        result['imageUrl'] = image_url
        video_filename = os.path.basename(result['video_url'])
        video_url = os.path.join(self.media_url, video_filename)
        result['videoUrl'] = video_url
        del result['image_url']
        del result['video_url']
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
    static_url = '/static/'

    def get(self):
        videos = Video.query.all()
        result = self.video_schema.dumps(videos, many=True)
        result = json.loads(result)
        for item in result:
            image_filename = os.path.basename(item['image_url'])
            image_url = os.path.join(self.static_url, image_filename)
            item['imageUrl'] = image_url
        return result, 200

    def post(self):
        ret = {}, 200
        data = request.get_json()
        video_data = self.convert_timestamp_info(data)
        if not video_data:
            ret = {'msg': 'timestamp error'}, 400
            return ret
        else:
            video = self.video_schema.load(video_data)
            ret = self.video_schema.dump(video.save())
            return ret, 201

    @staticmethod
    def convert_timestamp_info(data):
        ret = True
        video_num = data.get('video_num')
        image_num = data.get('image_num')
        video_name = data.get('video_name')
        image_name = data.get('image_name')
        video_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], video_num)
        image_path = os.path.join(
            current_app.config['UPLOAD_FOLDER'], image_num)
        if not video_num or not os.path.exists(video_path):
            ret = False
        if not image_num or not os.path.exists(image_path):
            ret = False
        if ret:
            video_storage_path = os.path.join(
                current_app.config['VIDEO_STORAGE_PATH'],
                video_name
            )
            image_storage_path = os.path.join(
                current_app.config['IMAGE_STORAGE_PATH'],
                image_name
            )
            shutil.move(video_path, video_storage_path)
            shutil.move(image_path, image_storage_path)
            ret = dict()
            ret['video_url'] = video_storage_path
            ret['image_url'] = image_storage_path
            ret['title'] = data.get('title')
            ret['description'] = data.get('description')
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
