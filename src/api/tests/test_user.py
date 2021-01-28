"""
user api test suit
"""
import json
from http import HTTPStatus
from flask import url_for
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
    assert '/static/assets/default-avatar.jpg' == data.get('avatar_image')

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
