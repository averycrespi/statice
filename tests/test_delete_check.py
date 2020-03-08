from flask import url_for


def test_delete_check(client, session, check):
    session.add(check)
    session.commit()
    response = client.get(url_for("admin.delete_check", id=check.id))
    assert response.status_code == 200
    assert b"Delete" in response.data
    # TODO: test that check is actually deleted


def test_delete_missing_check(client):
    response = client.get(url_for("admin.delete_check", id=1337))
    assert response.status_code == 404
