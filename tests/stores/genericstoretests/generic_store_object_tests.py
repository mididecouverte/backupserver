def test_object(store):
    test_store_object(store)
    test_apps_object(store.apps)


def test_store_object(store):
    assert store
    assert store.apps
    assert store.reset
    assert store.clean

def test_apps_object(apps):
    assert apps.create
    assert apps.get_all
    assert apps.get
    assert apps.update
    assert apps.delete
    assert apps.reset
    assert apps.clean
