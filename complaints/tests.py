import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from django.test import Client
from django.test import TestCase
# Create your tests here.


def test_login_page(client):
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user(new_user):
    assert User.objects.get(username="user123") == new_user


@pytest.mark.django_db
def test_login(client, new_user):
    response = client.post('/login/', {'login': "user123", 'password': '1234567890qwertyuiop'})
    assert response['Location'] == '/panel/home/'

