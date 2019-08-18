from collections import OrderedDict

from flask import session


class TaskDTO(OrderedDict):
    pass


class TaskNotFound(Exception):
    pass


class Task(object):

    @classmethod
    def create_task(cls, label):
        new_id = max(session.get('last_task', 0), 1)
        task = TaskDTO(id=new_id, label=label, completed=False)
        cls.add_task_to_the_list_of_tasks(task)

        session['last_task'] = new_id + 1
        return task

    @classmethod
    def add_task_to_the_list_of_tasks(cls, task):
        tasks = session.get('tasks', {})
        tasks[str(task['id'])] = task
        session['tasks'] = tasks

    @classmethod
    def get_task_by_id(cls, uid):
        try:
            tasks = session.get('tasks', {})
            return tasks[str(uid)]
        except KeyError:
            raise TaskNotFound(f"Task does not exist with id: {uid}")

    @classmethod
    def get_all(cls):
        return list(session.get('tasks', {}).values())

    @classmethod
    def update_task(cls, uid, json):

        task = cls.get_task_by_id(uid)
        task['label'] = json.get('label', task['label'])
        task['completed'] = json.get('completed', task['completed'])

        cls.add_task_to_the_list_of_tasks(task)
        return task

    @classmethod
    def delete_task(cls, uid):
        try:
            tasks = session.get('tasks', {})
            del tasks[str(uid)]
            session['tasks'] = tasks
        except KeyError:
            raise TaskNotFound(f"Task does not exist with id: {uid}")
