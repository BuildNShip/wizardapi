import string
import random

from api.models import UserApis


def generate_unique_token():
    token = ''.join(random.choice(
        string.ascii_uppercase + string.digits) for _ in range(10))
    uniqe_confirm = UserApis.objects.filter(token=token)
    while uniqe_confirm:
        token = ''.join(random.choice(
            string.ascii_uppercase + string.digits) for _ in range(10))
        if not UserApis.objects.filter(token=token):
            break
    return token