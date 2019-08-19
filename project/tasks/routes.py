import json

from flask import request, Response, make_response

from project.tasks import tasks_blueprint
from project.tasks.exceptions import TaskNotFound
from project.tasks.models import Task

BAD_REQUEST_MSG = "Bad request! Not valid parameter found."


@tasks_blueprint.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({'error': 'Not found'}), 404)


@tasks_blueprint.errorhandler(500)
def not_found(error):
    return make_response(json.dumps({'error': 'Internal Server Error'}), 500)


@tasks_blueprint.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.get_all()
    return Response(json.dumps(tasks), status=200, mimetype='application/json')


@tasks_blueprint.route('/tasks', methods=['POST'])
def add_tasks():
    try:
        task = Task().create_task(request.json['label'])
    except KeyError:
        return Response(json.dumps({'error': BAD_REQUEST_MSG}), status=400)
    output = {
        'task': task
    }

    return Response(json.dumps(output), status=201, mimetype='application/json')


@tasks_blueprint.route('/tasks/<int:uid>', methods=['POST'])
def update_task(uid):
    try:
        task = Task().update_task(uid, request.json.get('label'), request.json.get('completed'))

        output = {
            'task': task
        }
        return Response(json.dumps(output), status=201, mimetype='application/json')
    except TaskNotFound as ex:
        return Response(json.dumps({'error': str(ex)}), status=404, mimetype='application/json')
    except KeyError:
        return Response(json.dumps({'error': BAD_REQUEST_MSG}), status=400, mimetype='application/json')


@tasks_blueprint.route('/tasks/<int:uid>', methods=['DELETE'])
def delete_task(uid):
    try:
        task = Task.delete_task(uid)

        output = {
            'task': task
        }
        return Response(json.dumps(output), status=204, mimetype='application/json')
    except TaskNotFound as ex:
        return Response(json.dumps({'error': str(ex)}), status=404, mimetype='application/json')
