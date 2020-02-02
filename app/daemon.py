from flask import current_app


def wake_up():
    current_app.logger.info("I am awake!")
