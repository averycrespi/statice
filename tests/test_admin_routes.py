from flask import url_for

from app.models import Check


def test_empty_manage_checks(client):
    """
    WHEN there are no checks
        AND a GET request is sent to manage_checks
    THEN the request should succeed
    """
    r = client.get(url_for("admin.manage_checks"))
    assert r.status_code == 200
    assert b"Create" in r.data


def test_manage_checks_with_check(client, db, check):
    """
    GIVEN an existing check
    WHEN a GET request is sent to manage_checks
    THEN the request should succeed
        AND the check should appear on the page
    """
    db.session.add(check)
    db.session.commit()
    r = client.get(url_for("admin.manage_checks"))
    assert r.status_code == 200
    assert check.name in str(r.data)
    assert check.url in str(r.data)
    assert b"Edit" in r.data
    assert b"Delete" in r.data


def test_get_create_check(client):
    """
    WHEN a GET request is sent to create_check
    THEN the request should succeed
    """
    r = client.get(url_for("admin.create_check"))
    assert r.status_code == 200
    assert b"Name" in r.data
    assert b"URL" in r.data
    assert b"Create" in r.data


def test_post_create_check(client, db, check):
    """
    GIVEN a new check
    WHEN a POST request is sent to create_check
    THEN the request should succeed
        AND the check should be created
    """
    assert Check.query.filter_by(id=check.id).first() is None
    r = client.post(
        url_for("admin.create_check"),
        data={"name": check.name, "url": check.url},
        follow_redirects=True,
    )
    assert r.status_code == 200
    assert Check.query.filter_by(id=check.id).first() is not None


def test_get_edit_check(client, db, check):
    """
    GIVEN an existing check
    WHEN a GET request is sent to edit_check
    THEN the request should succeed
        AND the check should appear on the page
    """
    db.session.add(check)
    db.session.commit()
    r = client.get(url_for("admin.edit_check", id=check.id))
    assert r.status_code == 200
    assert b"Name" in r.data
    assert check.name in str(r.data)
    assert b"URL" in r.data
    assert check.url in str(r.data)
    assert b"Save" in r.data


def test_post_edit_check(client, db, check):
    """
    GIVEN an existing check
    WHEN a POST request is sent to edit_check
    THEN the request should succeed
        AND the check should be edited
    """
    db.session.add(check)
    db.session.commit()
    r = client.post(
        url_for("admin.edit_check", id=check.id),
        data={"name": check.name, "url": check.url},
        follow_redirects=True,
    )
    assert r.status_code == 200
    # TODO: check for edits


def test_edit_missing_check(client):
    """
    GIVEN a new check
    WHEN a GET request is sent to edit_check
    THEN the request should fail
    """
    r = client.get(url_for("admin.edit_check", id=1337))
    assert r.status_code == 404


def test_get_delete_check(client, db, check):
    """
    GIVEN an existing check
    WHEN a GET request is sent to delete_check
    THEN the request should succeed
        AND the check should appear on the page
    """
    db.session.add(check)
    db.session.commit()
    assert Check.query.filter_by(id=check.id).first() is not None
    r = client.get(url_for("admin.delete_check", id=check.id))
    assert r.status_code == 200
    assert check.name in str(r.data)
    assert b"Delete" in r.data


def test_post_delete_check(client, db, check):
    """
    GIVEN an existing check
    WHEN a POST request is sent to delete_check
    THEN the request should succeed
        AND the check should be deleted
    """
    db.session.add(check)
    db.session.commit()
    r = client.post(url_for("admin.delete_check", id=check.id), follow_redirects=True,)
    assert r.status_code == 200
    assert Check.query.filter_by(id=check.id).first() is None


def test_delete_missing_check(client, check):
    """
    GIVEN a new check
    WHEN a GET request is sent to delete_check
    THEN the request should fail
    """
    r = client.get(url_for("admin.delete_check", id=1337))
    assert r.status_code == 404
