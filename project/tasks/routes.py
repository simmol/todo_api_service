import json

from flask import request, Response
from project.tasks import tasks_blueprint
from project.tasks.models import Task, TaskNotFound


@tasks_blueprint.route('/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.get_all()
    print(tasks)
    return Response(json.dumps(tasks), status=200, mimetype='application/json')


@tasks_blueprint.route('/tasks', methods=['POST'])
def add_tasks():
    task = Task.create_task(request.json['label'])

    output = {
        'task': task
    }

    return Response(json.dumps(output), status=201, mimetype='application/json')


@tasks_blueprint.route('/tasks/<int:uid>', methods=['POST'])
def update_task(uid):
    try:
        task = Task.update_task(uid, request.json)

        output = {
            'task': task
        }
        return Response(json.dumps(output), status=201, mimetype='application/json')
    except TaskNotFound as ex:
        return Response(json.dumps({'error': str(ex)}), status=404, mimetype='application/json')


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
