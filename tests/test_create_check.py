from flask import url_for

from app.models import Check


def test_create_check(client, session, check):
    response = client.get(url_for("admin.create_check"))
    assert response.status_code == 200
    assert b"Name" in response.data
    assert b"URL" in response.data
    assert b"Create" in response.data
    response = client.post(
        url_for("admin.create_check"),
        data={"name": check.name, "url": check.url},
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert Check.query.filter_by(name=check.name).first() is not None
