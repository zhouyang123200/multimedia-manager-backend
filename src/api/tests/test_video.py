"""
title: video api test
description: all test suits for video api
"""
import os
import json
import pathlib
from shutil import copyfile
from http import HTTPStatus
from urllib.parse import urlencode
from api.models.video import VideoSchema, VideoFileSchema
from api.utils.database import db


def test_empty_db(app):
    """
    Start with a blank database.
    """

    rv = app.test_client().get('/api/videos')
    assert b'[]' in rv.data

def test_post_video(app, shared_datadir):
    """
    post a video item.
    """
    test_uri = '/api/videos'
    video_src = os.path.join(shared_datadir, 'sample.mp4')
    video_dst = os.path.join(app.config['UPLOAD_FOLDER'], '1608130297.1875458')
    copyfile(video_src, video_dst)
    image_src = os.path.join(shared_datadir, 'sample.jpg')
    image_dst = os.path.join(app.config['UPLOAD_FOLDER'], '1608130297.1875459')
    copyfile(image_src, image_dst)
    rv = app.test_client().post(test_uri, json={
        "title": 'test_video',
        'description': 'test video',
        'video_files': [{'num': '1608130297.1875458', 'name': 'test_video.mp4'}],
        'image_files': [{'num': '1608130297.1875459', 'name': 'test_image.jpg'}]
    })
    data = json.loads(rv.data)
    assert 'test_video' == data.get('title')
    assert 'test_video.mp4' in data.get('video_files')[0].get('url')

def test_put_video(app):
    """
    put a video entry
    """
    test_uri = '/api/video/1'
    video_data = {
        'title': 'video_one',
        'description': 'this is video description'
    }
    with app.app_context():
        video = VideoSchema().load(video_data)
        video.save()
    response = app.test_client().put(test_uri, json={'title': 'title_two'})
    data = json.loads(response.data)
    assert data.get('title') == 'title_two'
    response = app.test_client().\
        put(test_uri, json={'description': 'video description has changed'})
    data = json.loads(response.data)
    assert data.get('description') == 'video description has changed'


def test_get_videos(app):
    """
    test videos get api.
    """

    test_uri = '/api/videos'
    video_title = 'video'
    video_schema = VideoSchema()
    video_data = {
        'title': video_title,
        'video_files': [
            {'name': 'video_file_one', 'file_path': os.path.join(video_title, 'video_file_one')}
        ],
        'image_files': [
            {'name': 'image_file_one', 'file_path': os.path.join(video_title, 'image_file_one')}
        ],
        'description': 'test video description.'
    }

    with app.app_context():
        for num in range(10):
            data = video_data.copy()
            data['title'] = data['title'] + "_" + str(num)
            data['video_files'][0]['file_path'] = \
                 data['video_files'][0]['file_path'] + '_' + str(num)
            data['image_files'][0]['file_path'] = \
                 data['image_files'][0]['file_path'] + '_' + str(num)
            video_obj = video_schema.load(data)
            db.session.add(video_obj)
        db.session.commit()
    test_uri_with_args = test_uri + "?" + urlencode({'page': 1, 'per_page': 2})
    rv = app.test_client().get(test_uri_with_args)
    ret = json.loads(rv.data)
    assert rv.status_code == HTTPStatus.OK
    assert 'data' in ret
    assert ret.get('pages') == 5
    assert ret.get('links').get('next') == 'http://localhost' + test_uri +\
         '?' + urlencode({'page': 2, 'per_page': 2})

def test_subvideo_post(app, shared_datadir):
    """
    test video's subvideo post api
    """
    test_uri = '/api/video/1/subvideos'
    response = app.test_client().post(
        test_uri,
        json={'num': '1234', 'name': 'video name'}
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    with app.app_context():
        video = VideoSchema().load({
            'title': 'video title',
            'description': 'this is description',
        })
        video.save()
    video_src = os.path.join(shared_datadir, 'sample.mp4')
    video_dst = os.path.join(app.config['UPLOAD_FOLDER'], '1608130297.1875458')
    copyfile(video_src, video_dst)
    response = app.test_client().post(
        test_uri,
        json={'num': '1608130297.1875458', 'name': 'myvideo.mp4'}
    )
    print(response.data)
    assert response.status_code == HTTPStatus.OK
    data = response.get_json()
    print(data)
    assert data.get('video_files')[0]['name'] == 'myvideo.mp4'

def test_subvideo_delete(app, shared_datadir):
    """
    test subvideo delete api
    """
    test_uri = '/api/video/1/subvideos/myvideo.mp4'
    response = app.test_client().delete(test_uri)
    assert response.status_code == HTTPStatus.NOT_FOUND
    with app.app_context():
        video = VideoSchema().load({
            'title': 'video title',
            'description': 'this is a description'
        })
        video.save()
        video_dst = os.path.join(app.config['FILE_STORAGE_PATH'], video.title, 'myvideo.mp4')
        video_src = os.path.join(shared_datadir, 'sample.mp4')
        pathlib.Path(os.path.dirname(video_dst)).mkdir(parents=True, exist_ok=True)
        copyfile(video_src, video_dst)
        subvideo = VideoFileSchema().load({
            'name': 'myvideo.mp4',
            'file_path': video_dst
        })
        video.video_files.append(subvideo)
        video.save()
    response = app.test_client().delete(test_uri)
    assert response.status_code == HTTPStatus.NO_CONTENT
    response = app.test_client().delete(test_uri)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert not os.path.exists(video_dst)

def test_api_limiter(app):
    """
    test api rate limiter
    """

    for i in range(1, 250):
        response = app.test_client().get('/api/videos')
        if i == 201:
            assert response.status_code == HTTPStatus.TOO_MANY_REQUESTS
