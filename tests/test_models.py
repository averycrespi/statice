from app.models import Check, Status


def test_check(session):
    check = Check(name="Example", url="https://example.com", status=Status.INFO)
    session.add(check)
    print(check)
