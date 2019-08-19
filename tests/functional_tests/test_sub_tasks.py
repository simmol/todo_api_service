def test_sub_tasks_empty_at_start(test_client):
    """
    GIVEN a Flask application
    WHEN the '/tasks/<int:id>' page is requested (GET)
    THEN check the response is valid
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        test_client.post('/tasks', json={'label': "task"})
        response = test_client.get('/tasks/1')
        assert response.status_code == 200
        assert b'[]' in response.data


def test_add_sub_tasks_and_see_them_in_sub_tasks_list(test_client):
    with test_client.session_transaction() as sass:
        sass.clear()

        test_client.post('/tasks', json={'label': "task"})

        response = test_client.post('/tasks', json={'label': 'sub task', 'parent_task': 1})
        assert response.status_code == 201
        assert b'{"task": {"id": 2, "label": "sub task", "completed": false, "parent_task": 1}}' == response.data

        response = test_client.post('/tasks', json={'label': 'sub task two', 'parent_task': 1})
        assert response.status_code == 201
        assert b'{"task": {"id": 3, "label": "sub task two", "completed": false, "parent_task": 1}}' == response.data

        response = test_client.get('/tasks/1')
        assert response.status_code == 200
        assert b'[{"completed": false, "id": 2, "label": "sub task", "parent_task": 1}, {"completed": false, "id": 3, "label": "sub task two", "parent_task": 1}]' in response.data


def test_add_sub_task_of_sub_task_and_see_it_in_sub_tasks_list(test_client):
    with test_client.session_transaction() as sass:
        sass.clear()

        test_client.post('/tasks', json={'label': "task"})

        response = test_client.post('/tasks', json={'label': 'sub task', 'parent_task': 1})
        assert response.status_code == 201
        assert b'{"task": {"id": 2, "label": "sub task", "completed": false, "parent_task": 1}}' == response.data

        response = test_client.post('/tasks', json={'label': 'sub task of sub task', 'parent_task': 2})
        assert response.status_code == 201
        assert b'{"task": {"id": 3, "label": "sub task of sub task", "completed": false, "parent_task": 2}}' == response.data

        response = test_client.get('/tasks/2')
        assert response.status_code == 200
        assert b'[{"completed": false, "id": 3, "label": "sub task of sub task", "parent_task": 2}]' in response.data
