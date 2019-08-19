from flask import session


class Storage(object):

    def get_new_id(self):
        return max(session.get('last_task', 0), 1)

    def save_task(self, task):
        self.add_task_to_the_list_of_tasks(task)
        session['last_task'] = task['id'] + 1

    @staticmethod
    def add_task_to_the_list_of_tasks(task):
        tasks = session.get('tasks', {})
        tasks[str(task['id'])] = task
        session['tasks'] = tasks

    def get_all(self):
        return session.get('tasks', {})

    def update(self, task):
        self.add_task_to_the_list_of_tasks(task)

    def delete(self, uid):
        tasks = self.get_all()
        del tasks[str(uid)]
        session['tasks'] = tasks
