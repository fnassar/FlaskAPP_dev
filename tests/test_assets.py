import pytest
from assets.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    res = client.get('/')
    assert res.status_code == 200
    assert b"Check the requests status in the network tab of the browser's development tool." in res.data


def test_unoptimized(client):
    res = client.get('/foo')
    assert res.status_code == 200
    assert b'Unoptimized' in res.data
    assert b'Foo' in res.data


def test_optimized(client):
    res = client.get('/bar')
    assert res.status_code == 200
    assert b'Optimized' in res.data
    assert b'Bar' in res.data
