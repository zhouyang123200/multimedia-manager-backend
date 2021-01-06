import json
from api.models import User, UserSchema
from api.utils.database import db
from api.routes.user import black_list

USERDATA = {
    'username': 'user1',
    'passwd': 'admin123',
    'email': 'user1@test.com'
}

def create_user(app):
    user = UserSchema().load(USERDATA)
    with app.app_context():
        user.save()
    return user

def test_post_user(app):
    test_uri = '/api/users'
    response = app.test_client().post(test_uri, json=USERDATA)
    data = json.loads(response.data)
    assert 'user1' == data.get('username')
    assert 'user1@test.com' == data.get('email')
    assert 'access_token' in data

def test_post_token(app):
    test_uri = '/api/token'
    user = create_user(app)
    client = app.test_client()
    responses = client.post(test_uri, json=USERDATA)
    data = json.loads(responses.data)
    assert 'access_token' in data

    test_uri = '/api/revoke'
    responses = client.post(test_uri, headers={'Authorization': 'Bearer {}'.format(data['access_token'])})
    assert responses.status_code == 200
    responses = client.post(test_uri, headers={'Authorization': 'Bearer {}'.format(data['access_token'])})
    assert responses.status_code == 401


def test_get_usersporfile(app):
    pass
