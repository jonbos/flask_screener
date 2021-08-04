from screener_app.db import get_db


def test_add_to_favorites(client, auth, app):
    auth.login()
    assert client.get('/user/').status_code == 200
    client.post('/user/add_favorite', data={'user_id': '1', 'ticker': 'AAPL'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM user_favorite').fetchone()[0]
        assert count == 2
