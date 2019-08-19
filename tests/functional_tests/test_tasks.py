def test_tasks_empty_at_start(test_client):
    """
    GIVEN a Flask application
    WHEN the '/tasks' page is requested (GET)
    THEN check the response is valid
    """
    with test_client.session_transaction() as sass:
        sass.clear()
        response = test_client.get('/tasks')
        assert response.status_code == 200
        assert b"[]" in response.data


def test_add_task(test_client):
    """
    GIVEN a Flask application
    WHEN POST is made to '/tasks'
    THEN check the response is valid
    """

    with test_client.session_transaction() as sass:
        sass.clear()
        response = test_client.post('/tasks', json={'label': "task"})
        assert response.status_code == 201

        assert b'{"task": {"id": 1, "label": "task", "completed": false, "parent_task": null}}' == response.data

        test_client.get('/tasks')
        assert b'{"task": {"id": 1, "label": "task", "completed": false, "parent_task": null}}' in response.data


def test_add_two_tasks_have_different_ids_and_show_in_tasks(test_client):
    with test_client.session_transaction() as sass:
        sass.clear()
        response = test_client.post('/tasks', json={'label': "task"})
        assert response.status_code == 201
        assert b'{"task": {"id": 1, "label": "task", "completed": false, "parent_task": null}}' == response.data

        response2 = test_client.post('/tasks', json={'label': "task_two"})
        assert response2.status_code == 201
        assert b'{"task": {"id": 2, "label": "task_two", "completed": false, "parent_task": null}}' == response2.data

        response_tasks = test_client.get('/tasks')
        assert b'[{"completed": false, "id": 1, "label": "task", "parent_task": null}, {"completed": false, "id": 2, "label": "task_two", "parent_task": null}]' == response_tasks.data


def test_update_task_work_when_given_label_and_completed(test_client):
    """
    POST /tasks/:id
    PAYLOAD: { label: string, completed: boolean }
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        # Create two tasks
        test_client.post('/tasks', json={'label': "task"})
        test_client.post('/tasks', json={'label': "task_two"})

        # Update Task 2
        update_response = test_client.post('/tasks/2', json={'label': "task_two_v2", 'completed': True})
        assert update_response.status_code == 201
        assert b'{"task": {"completed": true, "id": 2, "label": "task_two_v2", "parent_task": null}}' == update_response.data

        response_tasks = test_client.get('/tasks')
        assert b'[{"completed": false, "id": 1, "label": "task", "parent_task": null}, {"completed": true, "id": 2, "label": "task_two_v2", "parent_task": null}]' == response_tasks.data


def test_update_task_work_when_given_label_only(test_client):
    """
    POST /tasks/:id
    PAYLOAD: { label: string }
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        # Create two tasks
        test_client.post('/tasks', json={'label': "task"})
        test_client.post('/tasks', json={'label': "task_two"})

        # Update Task 2
        update_response = test_client.post('/tasks/2', json={'label': "task_two_v2"})
        assert update_response.status_code == 201
        assert b'{"task": {"completed": false, "id": 2, "label": "task_two_v2", "parent_task": null}}' == update_response.data

        response_tasks = test_client.get('/tasks')
        assert b'[{"completed": false, "id": 1, "label": "task", "parent_task": null}, {"completed": false, "id": 2, "label": "task_two_v2", "parent_task": null}]' == response_tasks.data


def test_update_task_work_when_given_completed_only(test_client):
    """
    POST /tasks/:id
    PAYLOAD: { completed: boolean }
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        # Create two tasks
        test_client.post('/tasks', json={'label': "task"})
        test_client.post('/tasks', json={'label': "task_two"})

        # Update Task 2
        update_response = test_client.post('/tasks/2', json={'completed': True})
        assert update_response.status_code == 201
        assert b'{"task": {"completed": true, "id": 2, "label": "task_two", "parent_task": null}}' == update_response.data

        response_tasks = test_client.get('/tasks')
        assert b'[{"completed": false, "id": 1, "label": "task", "parent_task": null}, {"completed": true, "id": 2, "label": "task_two", "parent_task": null}]' == response_tasks.data


def test_update_task_return_404_and_error_msg_when_trying_to_update_not_existing_task(test_client):
    """
        POST /tasks/:id
        PAYLOAD: { completed: boolean }
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        # Create two tasks
        test_client.post('/tasks', json={'label': "task"})
        test_client.post('/tasks', json={'label': "task_two"})

        # Update Task 2
        update_response = test_client.post('/tasks/22', json={'completed': True})
        assert update_response.status_code == 404
        assert b'{"error": "Task does not exist with id: 22"}' == update_response.data


def test_delete_task(test_client):
    """
    DELETE /tasks/:id
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        # Create two tasks
        test_client.post('/tasks', json={'label': "task"})
        test_client.post('/tasks', json={'label': "task_two"})

        # Delete Task 1
        update_response = test_client.delete('/tasks/1')
        assert update_response.status_code == 204

        # Test that only task two is in the list
        response_tasks = test_client.get('/tasks')
        assert b'[{"completed": false, "id": 2, "label": "task_two", "parent_task": null}]' == response_tasks.data


def test_delete_task_return_404_and_error_msg_when_trying_to_delete_not_existing_task(test_client):
    """
    DELETE /tasks/:id
    """
    with test_client.session_transaction() as sass:
        sass.clear()

        # Create two tasks
        test_client.post('/tasks', json={'label': "task"})
        test_client.post('/tasks', json={'label': "task_two"})

        # Delete Task 1
        update_response = test_client.delete('/tasks/11')
        assert update_response.status_code == 404
        assert b'{"error": "Task does not exist with id: 11"}' == update_response.data
