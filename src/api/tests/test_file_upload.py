import hashlib
import io
import json


def md5(file):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read_bytes(4096), b''):
        hash_md5.update(chunk)
    return hash_md5.hexdigest()


def test_file_upload(app, shared_datadir):
    f_video = (shared_datadir / 'sample.mp4')
    f_video_stream = io.BytesIO()
    f_video_stream.write(f_video.read_bytes())
    client = app.test_client()

    rv = client.post('/api/files', input_stream=f_video_stream)
    data = json.loads(rv.data)
    assert 'timestamp' in data
    timestamp = data['timestamp']
    assert '.' in timestamp
    timestamp_0, timestamp_1 = timestamp.split('.')
    assert timestamp_0.isdigit() and timestamp_1.isdigit()
