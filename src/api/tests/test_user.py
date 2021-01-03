import json
from api.models import User, UserSchema
from api.utils.database import db

USERDATA = {
    'username': 'user1',
    'passwd': 'admin123',
    'email': 'user1@test.com'
}

def test_post_user(app):
    test_uri = '/api/users'
    response = app.test_client().post(test_uri, json=USERDATA)
    data = json.loads(response.data)
    assert 'user1' == data.get('username')
    assert 'user1@test.com' == data.get('email')
    assert 'access_token' in data

def test_post_token(app):
    test_uri = '/api/token'
    user = UserSchema().load(USERDATA)
    with app.app_context():
        user.save()
    responses = app.test_client().post(test_uri, json=USERDATA)
    data = json.loads(responses.data)
    assert 'access_token' in data

def test_get_usersporfile(app):
    pass
