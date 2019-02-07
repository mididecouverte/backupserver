import os
from app import App
import hashlib
import random
import os

class Apps(object):

    def __init__(self, store, data_path):
        self._store = store
        self._data_path = data_path

    def add(self, name, max_count=10):
        app = self.get(name)
        if not app:
            print('Create app', name)
            path = os.path.join(self._data_path, name)
            os.makedirs(path, exist_ok=True)
            self._store.apps.create(name, path, max_count)
        return App(self._store, name)

    @property
    def list(self):
        result = []
        apps = self._store.apps.get_all()
        for app in apps:
            result.append(App(self._store, app['name']))
        print(result)
        return result
    
    @property
    def count(self):
        return len(self.list)
    
    def remove(self, name):
        app = self.get(name)
        os.removedirs(app.path)
        self._store.apps.delete(name)
    
    def get(self, name):
        if not name:
            return None
        app = self._store.apps.get(name)
        if app:
            return App(self._store, app['name'])
        return None