import pytest
from database.app import app, db, Note
import sys

app.config['WTF_CSRF_ENABLED'] = False


@pytest.fixture
def client():
    app.config['TESTING'] = True

    WIN = sys.platform.startswith('win')
    if WIN:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_new_note_get(client):
    """Test the GET request to the new_note route"""
    res = client.get('/new')
    assert res.status_code == 200
    assert b'New Note' in res.data


@pytest.mark.order(1)
def test_new_note_post(client):
    """Test the POST request to the new_note route"""
    data = {
        'csrf_token': '',
        'body': 'Test Note',
        'submit': True
    }
    res = client.post('/new', data=data, follow_redirects=True)

    assert res.status_code == 200
    assert b'Your note is saved.' in res.data

    assert b'1 notes:' in res.data


@pytest.mark.order(2)
def test_edit_note(client):
    res = client.get('/')
    note = Note(body='Test Note')
    db.session.add(note)
    db.session.commit()

    res = client.get(f'/edit/{note.id}')
    assert res.status_code == 200
    assert b'Edit Note' in res.data

    assert b'Test Note' in res.data


@pytest.mark.order(3)
def test_edit_note_post(client):
    res = client.get('/')
    note = Note(body='Test Note')
    db.session.add(note)
    db.session.commit()

    data = {
        'csrf_token': '',
        'body': 'Updated Note',
        'submit': True
    }

    res = client.post(
        f'/edit/{note.id}', data=data, follow_redirects=True)
    assert res.status_code == 200
    assert b'Your note is updated.' in res.data
    assert b'Updated Note' in res.data

    with app.app_context():
        note = db.session.query(Note).filter_by(body='Updated Note').first()
        assert note is not None


@pytest.mark.order(4)
def test_delete_note_post(client):
    res = client.get('/')
    note = Note(body='Updated Note')
    db.session.add(note)
    db.session.commit()
    assert db.session.query(Note).count() == 1

    data = {
        'csrf_token': '',
        'submit': True
    }

    res = client.post(f'/delete/{note.id}', data=data, follow_redirects=True)

    assert res.status_code == 200
    assert b'Your note is deleted.' in res.data

    res = client.get('/')
    assert b'Updated Note' not in res.data
