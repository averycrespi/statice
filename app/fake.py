import faker.providers.lorem
import faker.providers.internet

from app.models import Category, Check, Event


def fake_category(faker):
    return faker.random_element(
        (Category.FAILURE, Category.INFO, Category.SUCCESS, Category.WARNING)
    )


def fake_check(faker):
    return Check(
        name=faker.word().title(),
        url=faker.uri(),
        status=fake_category(faker),
        interval=faker.random_int(min=1, max=60),
        retries=faker.random_int(min=0, max=5),
        timeout=faker.random_int(min=3, max=10),
    )


def fake_event(faker, check):
    return Event(
        check_id=check.id,
        category=fake_category(faker),
        message=faker.sentence().strip("."),
    )
