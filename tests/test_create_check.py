from flask import url_for


def test_create_check(client):
    response = client.get(url_for("admin.create_check"))
    assert response.status_code == 200
    assert b"Name" in response.data
    assert b"URL" in response.data
    assert b"Create" in response.data
