from collections import OrderedDict

from flask import session

from project.tasks.exceptions import TaskNotFound
from project.tasks.storage import Storage


class TaskDTO(OrderedDict):
    pass


class Task(object):
    storage = Storage()

    @classmethod
    def create_task(cls, label, parent_task_uid=None):
        if parent_task_uid:
            cls.get_task_by_id(parent_task_uid)

        task = TaskDTO(id=cls.storage.get_new_id(), label=label, completed=False, parent_task=parent_task_uid)
        cls.storage.save_task(task)
        return task

    @classmethod
    def get_task_by_id(cls, uid):
        try:
            tasks = session.get('tasks', {})
            return tasks[str(uid)]
        except KeyError:
            raise TaskNotFound(f"Task does not exist with id: {uid}")

    @classmethod
    def get_all(cls):
        return list(cls.storage.get_all().values())

    @classmethod
    def update_task(cls, uid, label=None, completed=None):

        task = cls.get_task_by_id(uid)
        task['label'] = label or task['label']
        task['completed'] = completed or task['completed']

        cls.storage.update(task)
        return task

    @classmethod
    def delete_task(cls, uid):
        try:
            cls.storage.delete(uid)
        except KeyError:
            raise TaskNotFound(f"Task does not exist with id: {uid}")

    @classmethod
    def get_all_sub_tasks_of_task(cls, uid):
        return cls.storage.get_sub_tasks_by_parent_task(uid)
