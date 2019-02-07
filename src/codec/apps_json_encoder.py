import json
from .app_json_encoder import AppJsonEncoder


class AppsJsonEncoder():

    def __init__(self, apps):
        self._apps = apps

    def encode(self, format='string'):
        result = {}
        result['count'] = self._apps.count
        apps = []
        for app in self._apps.list:
            apps.append(AppJsonEncoder(app).encode('dict'))
        result['apps'] = apps
        if format == 'dict':
            return result
        return json.dumps(result)
