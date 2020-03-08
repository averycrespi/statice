from flask import url_for


def test_empty_manage_checks(client):
    response = client.get(url_for("admin.manage_checks"))
    assert response.status_code == 200
    assert b"Create" in response.data


def test_manage_checks_with_check(client, session, check):
    session.add(check)
    session.commit()
    response = client.get(url_for("admin.manage_checks"))
    assert response.status_code == 200
    assert check.name in str(response.data)
    assert check.url in str(response.data)
    assert b"Edit" in response.data
    assert b"Delete" in response.data
