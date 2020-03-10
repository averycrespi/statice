from flask import url_for

from app.models import Check, Status


def test_empty_manage_checks(client):
    response = client.get(url_for("admin.manage_checks"))
    assert response.status_code == 200
    assert b"Create" in response.data


def test_manage_checks_with_check(client, db, check):
    db.session.add(check)
    db.session.commit()
    response = client.get(url_for("admin.manage_checks"))
    assert response.status_code == 200
    assert check.name in str(response.data)
    assert check.url in str(response.data)
    assert b"Edit" in response.data
    assert b"Delete" in response.data


def test_create_check(client, db, check):
    assert Check.query.filter_by(name=check.name).first() is None
    get_response = client.get(url_for("admin.create_check"))
    assert get_response.status_code == 200
    assert b"Name" in get_response.data
    assert b"URL" in get_response.data
    assert b"Create" in get_response.data
    post_response = client.post(
        url_for("admin.create_check"),
        data={"name": check.name, "url": check.url},
        follow_redirects=True,
    )
    assert post_response.status_code == 200
    assert Check.query.filter_by(name=check.name).first() is not None


def test_edit_check(client, db, check):
    db.session.add(check)
    db.session.commit()
    response = client.get(url_for("admin.edit_check", id=check.id))
    assert response.status_code == 200
    assert b"Name" in response.data
    assert check.name in str(response.data)
    assert b"URL" in response.data
    assert check.url in str(response.data)
    assert b"Save" in response.data
    # TODO: test form


def test_edit_missing_check(client):
    response = client.get(url_for("admin.edit_check", id=1337))
    assert response.status_code == 404


def test_delete_check(client, db, check):
    db.session.add(check)
    db.session.commit()
    assert Check.query.filter_by(name=check.name).first() is not None
    get_response = client.get(url_for("admin.delete_check", id=check.id))
    assert get_response.status_code == 200
    assert b"Delete" in get_response.data
    post_response = client.post(
        url_for("admin.delete_check", id=check.id), follow_redirects=True,
    )
    assert post_response.status_code == 200
    assert Check.query.filter_by(name=check.name).first() is None


def test_delete_missing_check(client, check):
    response = client.get(url_for("admin.delete_check", id=1337))
    assert response.status_code == 404
