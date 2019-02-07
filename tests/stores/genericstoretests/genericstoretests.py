from .generic_store_object_tests import test_object
from .generic_store_apps_tests import test_apps


def store_tests(store):
    test_object(store)
    store.reset()
    test_apps(store.apps)
    store.reset()
