from flask import url_for

from app.models import Check


def test_delete_check(client, session, check):
    session.add(check)
    session.commit()
    response = client.get(url_for("admin.delete_check", id=check.id))
    assert response.status_code == 200
    assert b"Delete" in response.data
    response = client.post(
        url_for("admin.delete_check", id=check.id), follow_redirects=True,
    )
    assert response.status_code == 200
    assert Check.query.filter_by(name=check.name).first() is None


def test_delete_missing_check(client):
    response = client.get(url_for("admin.delete_check", id=1337))
    assert response.status_code == 404
