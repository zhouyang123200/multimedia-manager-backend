import os
import json
import pathlib
from shutil import copyfile
from api.models.video import VideoSchema
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

def test_get_videos(app, shared_datadir):
    """
    test videos get api.
    """

    test_uri = '/api/videos'
    video_title = 'video_one'
    video_one_filepath = os.path.join(app.config['FILE_STORAGE_PATH'], video_title)
    video_schema = VideoSchema()
    video_one = video_schema.load({
        'title': video_title,
        'video_files': [{'name': 'video_file_one', 'file_path': os.path.join(video_title, 'video_file_one')}],
        'image_files': [{'name': 'image_file_one', 'file_path': os.path.join(video_title, 'image_file_one')}],
        'description': 'test video description.'
    })
    with app.app_context():
        db.session.add(video_one)
        db.session.commit()
    rv = app.test_client().get(test_uri)
    ret = json.loads(rv.data)
    assert video_title == ret[0].get('title')



