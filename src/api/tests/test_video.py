import os
import json
from shutil import copyfile


def test_empty_db(app):
    """Start with a blank database."""

    rv = app.test_client().get('/api/videos')
    assert b'[]' in rv.data

def test_post_video(app, shared_datadir):
    """post a video item"""

    video_src = os.path.join(shared_datadir, 'sample.mp4')
    video_dst = os.path.join(app.config['UPLOAD_FOLDER'], '12345')
    copyfile(video_src, video_dst)
    image_src = os.path.join(shared_datadir, 'sample.jpg')
    image_dst = os.path.join(app.config['UPLOAD_FOLDER'], '56789')
    copyfile(image_src, image_dst)
    rv = app.test_client().post('/api/videos', json={
        "title": 'test_video',
        'description': 'test video',
        'video_files': [{'num': '12345', 'name': 'test_video.mp4'}],
        'image_files': [{'num': '56789', 'name': 'test_image.jpg'}]
    })
    data = json.loads(rv.data)
    assert 'test_video' == data.get('title')
    assert 'test_video.mp4' in data.get('video_files')[0].get('url')
