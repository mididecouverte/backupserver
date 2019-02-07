from src.codec.app_json_encoder import AppJsonEncoder
from src.apps import Apps
import json
from src.stores import SqliteStore


def test_app_json_encoder():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = apps.add('name', 20)
    jsonobj = AppJsonEncoder(a).encode('dict')
    assert jsonobj['name'] == "name"
    assert jsonobj['path'] == "/tmp/name"
    assert jsonobj['max_count'] == 20


def test_app_json_encoder_string():
    store = SqliteStore(':memory:')
    apps = Apps(store, '/tmp')
    a = apps.add('name', 20)
    jsonstr = AppJsonEncoder(a).encode('string')
    assert type(jsonstr) == str
    jsonobj = json.loads(jsonstr)
    assert jsonobj['name'] == "name"
    assert jsonobj['path'] == "/tmp/name"
    assert jsonobj['max_count'] == 20

