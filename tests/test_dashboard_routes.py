from flask import url_for


def test_empty_dashboard(client):
    response = client.get(url_for("dashboard.dashboard"))
    assert response.status_code == 200
    assert b"No checks found" in response.data


def test_dashboard_with_check(client, db, check):
    db.session.add(check)
    db.session.commit()
    response = client.get(url_for("dashboard.dashboard"))
    assert response.status_code == 200
    assert check.name in str(response.data)
    assert check.url in str(response.data)


def test_view_check(client, db, check):
    db.session.add(check)
    db.session.commit()
    response = client.get(url_for("dashboard.view_check", id=check.id))
    assert response.status_code == 200
    assert check.name in str(response.data)
    assert check.url in str(response.data)
    assert b"History" in response.data
    # TODO: test with responses


def test_view_missing_check(client):
    response = client.get(url_for("dashboard.view_check", id=1337))
    assert response.status_code == 404
