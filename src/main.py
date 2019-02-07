#!/usr/bin/python3
from flask import Flask, send_from_directory, request, redirect, make_response, jsonify
import os
import errors
from session_exception import SessionError
from stores import SqliteStore
from codec import AppJsonEncoder, AppsJsonEncoder
from apps import Apps

data_path = '../data'
application = Flask(__name__, static_url_path='')

def get_store():
    return SqliteStore()

def return_error(code):
    error = {}
    error['code'] = code
    resp = make_response(jsonify(error), 400)
    return resp

def init_folders():
    os.makedirs(data_path, exist_ok=True)

@application.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@application.route('/apps')
def get_apps():
    apps = Apps(get_store(), data_path)
    return AppsJsonEncoder(apps).encode()

@application.route('/apps', methods=['POST'])
def add_apps():
    if not request.json:
            return return_error(errors.ERROR_INVALID_REQUEST)
    if 'name' not in request.json:
        return return_error(errors.ERROR_MISSING_PARAMS)

    apps = Apps(get_store(), data_path)
    name = request.json["name"]
    max_count = 10
    if 'max_count' in request.json:
        max_count = int(request.json['max_count'])
    app = apps.get(name)
    if app:
        return return_error(errors.ERROR_INVALID_APP)
    app = apps.add(name, max_count)
    print('App created', app)
    app_dict = AppJsonEncoder(app).encode('dict')
    print(app_dict)
    return jsonify({'app': app_dict})

@application.route('/apps/<app_name>')
def get_app(app_name):
    apps = Apps(get_store(), data_path)
    app = apps.get(app_name)
    print(app)
    if not app:
        return return_error(errors.ERROR_INVALID_APP)
    app_dict = AppJsonEncoder(app).encode('dict')
    return jsonify({'app': app_dict})

@application.route('/apps/<app_name>', methods=['POST'])
def update_app(app_name):
    apps = Apps(get_store(), data_path)
    app = apps.get(app_name)
    if not app:
        return return_error(errors.ERROR_INVALID_APP)
    if 'max_count' in request.json:
        app.max_count = request.json['max_count']
    app_dict = AppJsonEncoder(app).encode('dict')
    return jsonify({'app': app_dict})

@application.route('/apps/<app_name>', methods=['DELETE'])
def delete_app(app_name):
    apps = Apps(get_store(), data_path)
    app = apps.get(app_name)
    if not app:
        return return_error(errors.ERROR_INVALID_APP)
    apps.remove(app_name)
    print('Delete')
    return jsonify({'result': True})

# @application.route('/apps/<app_name>/backups')
# def get_app_backups(app_name):
#     backups = Backups(get_store())
#     backups_list = backups.get_all(app_name)
#     return "GET app " + app_name + ' list'

# @application.route('/apps/<app_name>/latest')
# def get_app_latest_backupt(app_name):
#     return "GET app " + app_name + ' latest backup'

# @application.route('/apps/<app_name>/<backup_id>')
# def get_app_backup(app_name, backup_id):
#     return "GET app " + app_name + ' backup ' + backup_id

# @application.route('/apps/<app_name>/push', methods=['POST'])
# def push_app_backupt(app_name):
#     backup_file = request.files['backup_file']
#     return "push app" + app_name + ' new backup'

init_folders()

if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', port=5001)
