import pytest
from src.apps import Apps
from src.stores import SqliteStore


def test_app():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = apps.add('name', 20)
    assert a.name == 'name'
    assert a.path == '/tmp/name'
    assert a.max_count == 20


def test_update_user():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = apps.add('name', 20)

    a.max_count = 15
    assert a.max_count == 15