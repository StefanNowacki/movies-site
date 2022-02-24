import pytest
from django.contrib.auth.models import User
from django.db import models
from django.apps import apps

start = 'http://127.0.0.1:8000/'


@pytest.mark.django_db
@pytest.mark.parametrize('param', ['add_movie', ''])
def test_urls(client, param):
    response = client.get(start + param)
    assert response.status_code == 200


@pytest.mark.django_db
def test_log_in(client):
    User.objects.create_user('admin1', 'admin1@admin.pl', 'admin1')
    data = {"username": "admin1",
            "password": "admin1"}

    client.post(start + 'accounts/login/', data)
    # # assert response. == start + 'admin_view'
    user = User.objects.filter(username='admin1').first()
    assert user is not None
    assert user.is_authenticated


@pytest.mark.django_db
def test_add_movie(client):
    data = {'title': 'film1',
            'description': ' ',
            'rating': 2,
            'director': '1',
            }
    apps.get_model('moviessite_app', 'Director').objects.create(name='director1', surname='director1', rating=1)
    client.post(start + 'add_movie', data)
    movie = apps.get_model('moviessite_app', 'Movie').objects.filter(title='film1').exists()
    # print(apps.get_model('moviessite_app', 'Movie').objects.all())
    assert movie







