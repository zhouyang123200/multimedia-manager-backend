from . import client


def test_empty_db(client):
    """Start with a blank database."""

    rv = client.get('/api/videos')
    assert b'[]' in rv.data
