from flask import session


class Storage(object):

    @staticmethod
    def get_new_id():
        return max(session.get('last_task', 0), 1)

    def save_task(self, task):
        if task['parent_task']:
            self.add_task_to_list_of_sub_tasks(task)

        self.add_task_to_the_list_of_tasks(task)
        session['last_task'] = task['id'] + 1

    @staticmethod
    def add_task_to_the_list_of_tasks(task):
        tasks = session.get('tasks', {})
        tasks[str(task['id'])] = task
        session['tasks'] = tasks

    @staticmethod
    def get_all():
        return session.get('tasks', {})

    @staticmethod
    def get_all_sub_tasks():
        return session.get('sub_tasks', {})

    def get_sub_tasks_by_parent_task(self, parent_task):
        sub_tasks = self.get_all_sub_tasks()
        return list(sub_tasks.get(str(parent_task), {}).values())

    def update(self, task):
        if task['parent_task']:
            self.add_task_to_list_of_sub_tasks(task)
        self.add_task_to_the_list_of_tasks(task)

    def delete(self, uid):
        tasks = self.get_all()
        del tasks[str(uid)]
        session['tasks'] = tasks

    def add_task_to_list_of_sub_tasks(self, task):
        sub_tasks = self.get_all_sub_tasks()

        parent_task_sub_tasks = sub_tasks.get(str(task['parent_task']), {})
        parent_task_sub_tasks[str(task['id'])] = task
        sub_tasks[str(task['parent_task'])] = parent_task_sub_tasks
        session['sub_tasks'] = sub_tasks
