"""
video apis
"""
import os
import pathlib
import shutil
import http
import time
from flask import Blueprint, request, current_app
from flask_restful import Api, Resource
from sqlalchemy import desc
from webargs import fields
from webargs.flaskparser import use_kwargs
from api.models import VideoSchema, VideoRawSchema, Video, VideoPaginationSchema
from api.utils.request_validate import mash_load_validate
from api.utils.limiter import limiter

video_route = Blueprint('video_route', __name__)
video_api = Api(video_route)


class VideoItem(Resource):
    """
    video rest api
    """

    video_schema = VideoSchema()
    static_url = '/static/'
    media_url = '/media/'

    def get(self, video_id):
        """
        video get api
        """
        video = Video.query.get(video_id)
        result = self.video_schema.dump(video)
        return result, http.HTTPStatus.OK

    def put(self, vedio_id):
        """
        video put api
        """
        video = Video.query.get(vedio_id)
        data = request.get_json()
        for key in video:
            if key in data:
                setattr(video, key, data.get(key))
        video.save()
        result = self.video_schema.dump(video)
        return result, http.HTTPStatus.NO_CONTENT

    def delete(self, video_id):
        """
        video delete api
        """
        video = Video.query.get(video_id)
        if video:
            video.delete()
            current_app.logger.warning('video %s delete successfully', video.title)
        return {}, http.HTTPStatus.NO_CONTENT


class VideoList(Resource):
    """
    video list api
    """

    video_schema = VideoSchema()
    video_pagenation_schema = VideoPaginationSchema()
    raw_video_schema = VideoRawSchema()
    decorators = [limiter.limit('200 per minute', methods=['GET'], error_message='Too Many Requests')]

    @use_kwargs({'page': fields.Int(missing=1),
                            'query': fields.Str(missing=''),
                           'per_page': fields.Int(missing=5)}, location='query')
    def get(self, query, page, per_page):
        """
        video list get api
        """
        keyword = f'%{query}%'
        videos = Video.query.filter(Video.title.ilike(keyword)).\
            order_by(desc(Video.created_at)).\
            paginate(page=page, per_page=per_page)
        ret = self.video_pagenation_schema.dump(videos)
        return ret, http.HTTPStatus.OK

    def post(self):
        """
        video create api
        """
        data = request.get_json()
        data = mash_load_validate(self.raw_video_schema, data)
        video_data = self.convert_timestamp_info(data)
        video = mash_load_validate(self.video_schema, video_data)
        ret = self.video_schema.dump(video.save())
        current_app.logger.info('video %s created successfully', video.title)
        return ret, http.HTTPStatus.CREATED

    @staticmethod
    def convert_timestamp_info(data):
        """
        move related file from upload file path to storage file path
        """
        videos = data.get('video_files')
        images = data.get('image_files')

        # judge the exits of video and images
        upload_path = current_app.config['UPLOAD_FOLDER']
        storage_path = current_app.config['FILE_STORAGE_PATH']
        title = data.get('title')
        storage_dir = os.path.join(storage_path, title)

        pathlib.Path(storage_dir).mkdir(parents=True, exist_ok=True)

        for video in videos:
            video_name = video.get('name')
            video_upload_path = os.path.join(upload_path, video.get('num'))
            video_storage_path = os.path.join(storage_dir, video_name)
            shutil.move(video_upload_path, video_storage_path)
            video['file_path'] = os.path.join(title, video_name)
            del video['num']

        for image in images:
            image_name = image.get('name')
            image_upload_path = os.path.join(upload_path, image.get('num'))
            image_storage_path = os.path.join(storage_dir, image_name)
            shutil.move(image_upload_path, image_storage_path)
            image['file_path'] = os.path.join(title, image_name)
            del image['num']

        return data


class UploadFiles(Resource):
    """
    file upload api
    swagger_from_file: file/file_post.yml
    """

    def post(self):
        """
        post api for file upload
        """
        filename = str(time.time())
        filepath = os.path.join(
            os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        with open(filepath, 'bw') as uploadfile:
            chunk_size = 1024
            while True:
                chunk = request.stream.read(chunk_size)
                if len(chunk) == 0:
                    break
                uploadfile.write(chunk)
        current_app.logger.info('file %s upload successfully', filename)
        return {'timestamp': filename}, http.HTTPStatus.CREATED


video_api.add_resource(VideoItem, '/api/video/<int:id>')
video_api.add_resource(VideoList, '/api/videos')
video_api.add_resource(UploadFiles, '/api/files')
