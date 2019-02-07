from src.stores.sqlite import SqliteStore
from genericstoretests import store_tests


def test_sqlite_store():
    store = SqliteStore(':memory:')
    store_tests(store)
