import uuid
import datetime


def generate_token():
    return str(uuid.uuid4())


def generate_expiration():
    return datetime.datetime.now() + datetime.timedelta(minutes=30)
