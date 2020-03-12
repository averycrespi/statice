from flask import url_for


def test_dashboard_with_no_checks(client):
    """
    WHEN there are no checks
        AND a GET request is sent to the dashboard
    THEN the request should succeed
        AND the page should indicate that there are no checks
    """
    r = client.get(url_for("dashboard.dashboard"))
    assert r.status_code == 200
    assert b"No checks found" in r.data


def test_dashboard_with_check(client, db, check):
    """
    GIVEN an existing check
    WHEN a GET request is sent to the dashboard
    THEN the request should succeed
        AND the check should appear on the page
    """
    db.session.add(check)
    db.session.commit()
    r = client.get(url_for("dashboard.dashboard"))
    assert r.status_code == 200
    assert check.name in str(r.data)
    assert check.url in str(r.data)


def test_view_check(client, db, check, response):
    """
    GIVEN an existing check and an associated response
    WHEN a GET request is sent to view_check
    THEN the request should succeed
        AND the check should appear on the page
        AND the response should appear on the page
    """
    db.session.add_all((check, response))
    db.session.commit()
    r = client.get(url_for("dashboard.view_check", id=check.id))
    assert r.status_code == 200
    assert check.name in str(r.data)
    assert check.url in str(r.data)
    assert b"History" in r.data
    assert response.description in str(r.data)


def test_view_missing_check(client, check):
    """
    GIVEN a new check
    WHEN a GET request is sent to view_check
    THEN the request should fail
    """
    r = client.get(url_for("dashboard.view_check", id=check.id))
    assert r.status_code == 404
