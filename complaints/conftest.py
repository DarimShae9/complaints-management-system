import pytest
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.fixture
def client():
    client = Client()
    return client


@pytest.fixture
def new_user():
    ctx = {
        'is_active': 1
    }
    user = User.objects.create_user(
        username='user123',
        email='dfdsfs@sds.pl',
        password='1234567890qwertyuiop',
        **ctx
    )
    return user
