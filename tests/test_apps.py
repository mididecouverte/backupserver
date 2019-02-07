from src.apps import Apps
from src.stores import SqliteStore


def generate_app(apps):
    return apps.add('name', 20)


def test_add_app():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = generate_app(apps)
    assert a
    assert apps.count == 1
    assert apps.list[0] == a
    ga = apps.get('name')
    assert ga
    assert ga == a
    ga = apps.get('test2')
    assert not ga


def test_double_add_user():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = apps.add('test', 20)
    a2 = apps.add('test', 30)
    assert a
    assert a2
    assert a == a2
    assert apps.count == 1
    assert apps.list[0] == a


def test_remove_user():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = generate_app(apps)
    apps.remove(a.name)
    assert apps.count == 0
    ga = apps.get('test')
    assert not ga




