import secrets
import random


def new_token_url(length):
    return secrets.token_urlsafe(length)


def random_token_url(start, end):
    length = random.randint(start, end)
    return new_token_url(length)
