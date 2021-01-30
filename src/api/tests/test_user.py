"""
user api test suit
"""
import json
import shutil
import os
from http import HTTPStatus
from flask import url_for
from flask_jwt_extended import create_access_token
from api.models import UserSchema
from api.utils.passwd import generate_token

USERDATA = {
    'username': 'user1',
    'passwd': 'admin123',
    'email': 'user1@test.com',
    'is_activate': True
}

def create_user(app):
    """
    tool fuction for create test user
    """
    user = UserSchema().load(USERDATA)
    with app.app_context():
        user.save()
        print(user)
    return user

def test_post_user(app):
    """
    test user post api
    """
    test_uri = '/api/users'
    response = app.test_client().post(test_uri, json=USERDATA)
    data = json.loads(response.data)
    assert USERDATA.get('username') == data.get('username')
    assert USERDATA.get('email') == data.get('email')

def test_post_token(app):
    """
    test post user data and get token api
    """
    test_uri = '/api/token'
    create_user(app)
    client = app.test_client()
    responses = client.post(test_uri, json=USERDATA)
    data = json.loads(responses.data)
    assert 'access_token' in data

    test_uri = '/api/revoke'
    responses = client.post(test_uri, headers={'Authorization': 'Bearer {}'.\
        format(data['access_token'])})
    assert responses.status_code == 200
    responses = client.post(test_uri, headers={'Authorization': 'Bearer {}'.\
        format(data['access_token'])})
    assert responses.status_code == 401

def test_activate_user(app):
    """
    test avtivate user api
    """
    user = create_user(app)
    with app.app_context():
        token = generate_token(email=USERDATA.get('email'), salt='activate')
        user.is_activate = False
        user.save()
    with app.test_request_context():
        test_uri = url_for('user_route.tokenresource', _external=False)
    response = app.test_client().post(test_uri, json=USERDATA)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    with app.test_request_context():
        test_uri = url_for('user_route.useractivateresource', token=token, _external=False)
    response = app.test_client().get(test_uri)
    assert response.status_code == HTTPStatus.NO_CONTENT

def test_put_avatar(app, shared_datadir):
    """
    test user avatar put api
    """
    user = create_user(app)
    with app.app_context():
        user_id = user.id
        access_token = create_access_token(identity=user_id, fresh=True)
    test_uri = '/api/user/avatar'
    timestamp = '1608130297.1875460'
    image_name = 'sample.jpg'

    client = app.test_client()
    avatar_src = os.path.join(shared_datadir, image_name)
    avatar_dst = os.path.join(app.config['UPLOAD_FOLDER'], timestamp)
    shutil.copyfile(avatar_src, avatar_dst)

    headers = {'Authorization': f'Bearer {access_token}'}
    data = {
        'file_name': timestamp,
        'image_name': image_name,
    }
    response = client.put(test_uri, headers=headers, json=data)
    data = json.loads(response.data)
    assert response.status_code == HTTPStatus.OK
    assert data.get('avatar_url') == f'/static/users/{user.username}/avatar/{image_name}'
