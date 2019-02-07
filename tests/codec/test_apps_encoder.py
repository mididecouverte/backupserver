from src.codec.apps_json_encoder import AppsJsonEncoder
from src.apps import Apps
from src.stores import SqliteStore
import json


def generate_app(apps):
    apps.add('test', 20)


def test_apps_json_encoder():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    generate_app(apps)
    jsonobj = AppsJsonEncoder(apps).encode('dict')
    assert jsonobj['count'] == 1
    assert len(jsonobj['apps']) == 1
