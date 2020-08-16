def test_empty_db(client):
    rv = client.get('/users/')
    assert b'No entries here so far' in rv.data
