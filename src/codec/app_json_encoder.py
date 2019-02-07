import json


class AppJsonEncoder():

    def __init__(self, app):
        self._app = app

    def encode(self, format='string'):
        result = {}
        result['name'] = self._app.name
        result['path'] = self._app.path
        result['max_count'] = self._app.max_count

        if format == 'dict':
            return result
        print('Encoder app', result)
        return json.dumps(result)
