
class App(object):

    def __init__(self, store, name):
        self._store = store
        self._name = name
    
    def get_data(self):
        return self._store.apps.get(self._name)

    def update_data(self, data):
        self._store.apps.update(self._name, data['path'],
                                 data['max_count'])
    
    @property
    def name(self):
        return self.get_data()['name']
    
    @property
    def path(self):
        return self.get_data()['path']
    
    @property
    def max_count(self):
        return self.get_data()['max_count']
    
    @max_count.setter
    def max_count(self, value):
        data = self.get_data()
        data['max_count'] = value
        self.update_data(data)
    
    def __eq__(self, value):
        return self.get_data() == value.get_data()