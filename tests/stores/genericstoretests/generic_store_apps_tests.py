def generate_app(apps):
    apps.create('test', '/tmp', 20)


def test_apps(apps):
    test_apps_app(apps)
    test_update(apps)
    test_delete(apps)
    test_reset(apps)
    test_clean(apps)


def test_apps_app(apps):
    generate_app(apps)
    assert len(apps.get_all()) == 1
    app = apps.get_all()[0]
    assert app
    assert apps.get('test')
    assert app == apps.get('test')
    assert app['name'] == 'test'
    assert app['path'] == '/tmp'
    assert app['max_count'] == 20
    apps.delete('test')


def test_update(apps):
    generate_app(apps)
    apps.update('test', '/tmp2', 15)
    assert len(apps.get_all()) == 1
    app = apps.get_all()[0]
    assert app
    assert app['name'] == 'test'
    assert app['path'] == '/tmp2'
    assert app['max_count'] == 15
    apps.delete('test')


def test_delete(apps):
    generate_app(apps)
    apps.delete('test')
    assert len(apps.get_all()) == 0
    assert not apps.get('test')
    apps.delete('test')


def test_reset(apps):
    generate_app(apps)
    apps.reset()
    assert len(apps.get_all()) == 0
    assert not apps.get('test')
    apps.reset()


def test_clean(apps):
    generate_app(apps)
    apps.clean()
    assert len(apps.get_all()) == 0
    assert not apps.get('test')
    apps.clean()
