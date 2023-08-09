import pytest
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()
from .models import Order, Company, Message

@pytest.fixture
def client():
    client = Client()
    return client




@pytest.fixture
def new_user():
    company = Company.objects.create(nip='123451')
    ctx = {
        'is_active': 1,
        'company_id': company.nip
    }
    user = User.objects.create_user(
        username='user123',
        email='dfdsfs@sds.pl',
        password='1234567890qwertyuiop',
        **ctx
    )
    return user


@pytest.fixture
def admin_user():
    ctx = {
        'is_active': 1,
        'is_staff': 1,
        'is_superuser': 1
    }
    user = User.objects.create_user(
        username='admin123',
        email='admin123@sds.pl',
        password='admin123',
        **ctx
    )
    return user


@pytest.fixture
def all_users():
    return User.objects.all()


@pytest.fixture
def order():
    company = Company.objects.create(
        name="asd",
        nip="123"
    )

    more_data = {
        'company_id': company.nip,
    }
    return Order.objects.create(
        number='12345',
        **more_data
    )


@pytest.fixture
def messages():
    return Message.objects.all()


@pytest.fixture
def all_order():
    return Order.objects.all()


@pytest.fixture
def company():
    return Company.objects.create(
        nip='123'
    )
