import json

def test_post_user(app):
    test_uri = '/api/users'
    data = {
        'username': 'user1',
        'passwd': 'admin123',
        'email': 'user1@test.com'
    }
    response = app.test_client().post(test_uri, json=data)
    data = json.loads(response.data)
    assert 'user1' == data.get('username')
    assert 'user1@test.com' == data.get('email')

def test_post_token(app):
    pass

def test_get_usersporfile(app):
    pass
