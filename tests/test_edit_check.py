from flask import url_for


def test_edit_check(client, session, check):
    session.add(check)
    session.commit()
    response = client.get(url_for("admin.edit_check", id=check.id))
    assert response.status_code == 200
    assert b"Name" in response.data
    assert check.name in str(response.data)
    assert b"URL" in response.data
    assert check.url in str(response.data)
    assert b"Save" in response.data
    # TODO: test that check is actually edited


def test_edit_missing_check(client):
    response = client.get(url_for("admin.edit_check", id=1337))
    assert response.status_code == 404
