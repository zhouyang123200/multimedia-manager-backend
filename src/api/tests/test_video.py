

def test_empty_db(app):
    """Start with a blank database."""

    rv = app.test_client().get('/api/videos')
    assert b'[]' in rv.data
