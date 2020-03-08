from flask import url_for


def test_empty_dashboard(client):
    response = client.get(url_for("dashboard.dashboard"))
    assert response.status_code == 200
    assert b"Home" in response.data
    assert b"Admin" in response.data
    assert b"No checks found" in response.data


def test_dashboard_with_check(client, session, check):
    session.add(check)
    session.commit()
    response = client.get(url_for("dashboard.dashboard"))
    assert response.status_code == 200
    assert check.name in str(response.data)
    assert check.url in str(response.data)
