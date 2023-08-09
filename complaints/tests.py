import pytest
from django.contrib.auth import get_user_model
User = get_user_model()
from pytest_django.asserts import assertQuerysetEqual
from .function import update_modification_time, historic_entry
from datetime import datetime
# Create your tests here.


def test_login_page(client):
    """testing the login page"""
    response = client.get('/login/')
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_user(new_user):
    """test user creation"""
    assert User.objects.get(username="user123") == new_user


@pytest.mark.django_db
def test_login(client, new_user):
    """testing whether logging works"""
    response = client.post('/login/', {'login': "user123", 'password': '1234567890qwertyuiop'})
    assert response['Location'] == '/panel/home/'


@pytest.mark.django_db
def test_admin_user(client, new_user):
    """test if an unusual user is not able to connect the page for the admin"""
    client.force_login(new_user)
    response = client.get('/adm/user/')
    assert 'admin/no_permissions.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_admin_user_for_admin(client, admin_user):
    """test if the admin has the ability to connect the page for the admin"""
    client.force_login(admin_user)
    response = client.get('/adm/user/')
    assert 'admin/user.html' in (t.name for t in response.templates)


@pytest.mark.django_db
def test_admin_user_loading_all_user(client, admin_user, all_users):
    """test if admin can load all users"""
    client.force_login(admin_user)
    response = client.get('/adm/user/')
    assertQuerysetEqual(response.context['users'], all_users)


@pytest.mark.django_db
def test_update_modification_time(order):
    """test whether the time update function works"""
    update_modification_time(order.id)
    assert order.modification_date <= datetime.now()


@pytest.mark.django_db
def test_historic_entry(order, new_user, messages):
    """test whether the history function works"""
    historic_entry(order.id, new_user, 'text')
    assert len(messages) == 1


@pytest.mark.django_db
def test_add_compaint_view(client, new_user, all_order):
    """checking if adding a complaint works"""
    client.force_login(new_user)
    client.post('/panel/add-compaint/', {'number': '123123'})
    assert len(all_order) == 1

